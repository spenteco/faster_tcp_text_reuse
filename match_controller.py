#!/home/spenteco/anaconda2/envs/py3/bin/python

import time, glob, psutil, subprocess

EEBO_SHINGLE_FOLDER = '/home/spenteco/0/eebo_shingled/'
OUTPUT_FOLDER = 'all_to_all_html_outputs/'
N_WORKERS = 6

def match_controller():

    print('starting match_controller', time.ctime(time.time()))

    all_processed_ids = []
    for p in glob.glob(OUTPUT_FOLDER + '/*.html'):
        all_processed_ids.append(p.split('/')[-1].split('.')[0])
    all_processed_ids = set(all_processed_ids)

    all_unprocessed_ids = []
    for p in glob.glob(EEBO_SHINGLE_FOLDER + '/*.pickle'):
        tcp_id = p.split('/')[-1].split('.')[0]
        if tcp_id not in all_processed_ids:
            all_unprocessed_ids.append(tcp_id)

    print('len(all_processed_ids)', len(all_processed_ids))
    print('len(all_unprocessed_ids)', len(all_unprocessed_ids))

    while True:
        
        try:
        
            time.sleep(1)

            n_match_workers_found_and_kept = 0

            for proc in psutil.process_iter():

                current_time = time.time()

                if 'match_worker' in proc.name():

                    run_time = current_time - proc.create_time()

                    if proc.memory_percent() > 25.0 or run_time > 120.0:
                        proc.kill()
                    else:
                        n_match_workers_found_and_kept += 1

        except psutil.NoSuchProcess:
            pass

        while n_match_workers_found_and_kept < N_WORKERS:
        
            n_match_workers_found_and_kept += 1

            next_tcp_id = all_unprocessed_ids.pop()
            cmd = 'export PYTHONUNBUFFERED=1; nohup ./match_worker.py ' + next_tcp_id + ' > stdout_and_err/' + next_tcp_id + '.txt 2>&1 &'
            print(cmd, subprocess.getoutput(cmd))
        
# ----------------------------------------------------------------------

if __name__ == "__main__":

    match_controller()
