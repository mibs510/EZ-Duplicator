#  Copyright (c) 2021 Connor McMillan. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
#  following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#  disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#  following disclaimer in the documentation and/or other materials provided with the distribution.
#
#  3. All advertising materials mentioning features or use of this software must display the following acknowledgement:
#  This product includes software developed by Connor McMillan.
#
#  4. Neither Connor McMillan nor the names of its contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY CONNOR MCMILLAN "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
#  EVENT SHALL CONNOR MCMILLAN BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
#  TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.

import logging
import multiprocessing
import sys
from multiprocessing import Process, Queue

from gi import require_version as gi_require_version

import EZDuplicator.lib.BPBDuplication
import EZDuplicator.lib.DataOnlyDuplication
import EZDuplicator.lib.EZDuplicator

gi_require_version('Gtk', '3.0')


def verification_process(pipe_connection, pids, failed_drives, option):
    logging.info("================== Begin Verification ==================")
    source_by_path = EZDuplicator.lib.EZDuplicator.get_source_by_path()
    source = EZDuplicator.lib.EZDuplicator.get_source_blkdev(source_by_path)
    targets = EZDuplicator.lib.EZDuplicator.get_number_or_list_of_usbs('list', source_by_path)
    number_of_targets = EZDuplicator.lib.EZDuplicator.get_number_or_list_of_usbs('number', source_by_path)
    processes = []
    number_of_processes = multiprocessing.cpu_count()

    """ Unmount everything """
    # logging.info("Starting to unmount each source and target...")
    # EZDuplicator.lib.DataOnlyDuplication.unmount_all_partitions(source)
    # for target in targets:
    #     EZDuplicator.lib.DataOnlyDuplication.unmount_all_partitions(target)
    # logging.info("Finished unmounting each source and target.")

    """ Clean mount(8) map """
    logging.info("Starting to clean mount points from mount(8)...")
    EZDuplicator.lib.DataOnlyDuplication.clean_mount_map()
    logging.info("Finished cleaning mount points from mount(8).")

    """ Clean the source """
    logging.info("Starting to clean source...")
    EZDuplicator.lib.DataOnlyDuplication.fsck(source)
    logging.info("Finished cleaning source.")

    """ Grab a list of the checksums from the source drive """
    list_of_source_xxhsums = []
    source_xxhash = ""
    if option == "DataOnlyVerification":
        logging.info("Get xxhsum hash(es) from source drive {}".format(source))
        list_of_source_xxhsums = EZDuplicator.lib.DataOnlyDuplication.get_list_of_xxhsums(source, failed_drives)
        logging.info("Finished getting xxhsum hash(es) from source drive {}".format(source))

        """ Enable the hint if the total used space on the source exceeds more than 250MB """
        if EZDuplicator.lib.DataOnlyDuplication.get_size_of_used_space(source) > 250000000:
            pipe_connection.send("LargeDataDetected")
    elif option == "BPBVerification":
        """ Get source drive hash for comparison """
        pipe_connection("LargeDataDetected")
        EZDuplicator.lib.DataOnlyDuplication.unmount_all_partitions(source)
        for target in targets:
            EZDuplicator.lib.DataOnlyDuplication.unmount_all_partitions(target)

        logging.info("Get xxhsum hash from source drive {}".format(source))
        source_xxhash = EZDuplicator.lib.EZDuplicator.get_xxhsum_hash(source, failed_drives)
        logging.info("xxhsum hash from source drive = {}".format(source_xxhash))
    pipe_connection.send("Bump")

    """ Did we fail to get checksum(s) from the source? """
    if source in failed_drives:
        logging.error("Cannot proceed! Failed to obtain checksum(s) from source!")
        pipe_connection.send("Stop")
        EZDuplicator.lib.EZDuplicator.sleep_indfinite()

    """ QA Queue """
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()

    for target in targets:
        tasks_to_accomplish.put(target)

    for w in range(number_of_processes):
        process = Process()
        if option == "DataOnlyVerification":
            process = Process(target=EZDuplicator.lib.DataOnlyDuplication.qa_task_manager, args=(tasks_to_accomplish,
                                                                                                 tasks_that_are_done,
                                                                                                 pipe_connection,
                                                                                                 source,
                                                                                                 list_of_source_xxhsums,
                                                                                                 failed_drives),
                              daemon=True)
        elif option == "BPBVerification":
            process = Process(target=EZDuplicator.lib.BPBDuplication.qa_task_manager, args=(tasks_to_accomplish,
                                                                                            tasks_that_are_done,
                                                                                            pipe_connection, source,
                                                                                            source_xxhash,
                                                                                            failed_drives),
                              daemon=True)
        processes.append(process)
        process.start()
        pids.append(process.pid)

    """ Completing process """
    for process in processes:
        process.join()

    while not tasks_that_are_done.empty():
        logging.info(tasks_that_are_done.get())

    tasks_that_are_done.close()
    tasks_to_accomplish.close()

    """ Unmount everything """
    # logging.info("Starting to unmount each source and target...")
    # EZDuplicator.lib.DataOnlyDuplication.unmount_all_partitions(source)
    # for target in targets:
    #     EZDuplicator.lib.DataOnlyDuplication.unmount_all_partitions(target)
    # logging.info("Finished unmounting each source and target.")

    EZDuplicator.lib.EZDuplicator.kill_pids(pids)

    """ Clean mount(8) map """
    logging.info("Starting to clean mount points from mount(8)...")
    EZDuplicator.lib.DataOnlyDuplication.clean_mount_map()
    logging.info("Finished cleaning mount points from mount(8).")

    """ Clean up directories in mnt/source & mnt/target """
    logging.info("Starting to clean source...")
    EZDuplicator.lib.DataOnlyDuplication.cleanup_dirs()
    logging.info("Finished cleaning source.")

    pipe_connection.send("Finished")

    if len(failed_drives) == 0:
        EZDuplicator.lib.EZDuplicator.send_email_notification(
            "Verification", "{} drive(s) verified".format(number_of_targets), "No mismatches found!", test=False)
    elif len(failed_drives) > 0:
        logging.debug("number_of_failed_drives = {}, failed_drives = {}".format(len(failed_drives), failed_drives))
        pipe_connection.send("Enable_QADialog_Button")
        EZDuplicator.lib.EZDuplicator.send_email_notification(
            "Verification", "{}/{} drive(s) failed".format(
                len(failed_drives), number_of_targets), "Mismatches found!", test=False)

    logging.info("================== End Verification ==================")


def cancel(number_of_usbs, pids, cancel_io_watch):
    try:
        cancel_io_watch.send("spinner")
        EZDuplicator.lib.EZDuplicator.kill_pids(pids)
        cancel_io_watch.send("terminate")

        """ Clean mount(8) map """
        logging.info("Starting to clean mount points from mount(8)...")
        EZDuplicator.lib.DataOnlyDuplication.clean_mount_map()
        logging.info("Finished cleaning mount points from mount(8).")

        EZDuplicator.lib.EZDuplicator.send_email_notification(
            "Verification", "Operator aborted {} drive(s) while verifying".format(
                number_of_usbs), "Incomplete", test=False)
        cancel_io_watch.send("destroy")
    except Exception as ex:
        logging.error(ex, exc_info=sys.exc_info())


def stop(pids, stop_io_watch):
    try:
        stop_io_watch.send("spinner")
        EZDuplicator.lib.EZDuplicator.kill_pids(pids)
        stop_io_watch.send("terminate")

        """ Clean mount(8) map """
        logging.info("Starting to clean mount points from mount(8)...")
        EZDuplicator.lib.DataOnlyDuplication.clean_mount_map()
        logging.info("Finished cleaning mount points from mount(8).")
        EZDuplicator.lib.EZDuplicator.send_email_notification(
            "Verification", "Review debug console for further details.", "Fatal Error Occured", test=False)
        stop_io_watch.send("stop")
    except Exception as ex:
        logging.error(ex, exc_info=sys.exc_info())
