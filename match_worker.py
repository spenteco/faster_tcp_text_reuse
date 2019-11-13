#!/home/spenteco/anaconda2/envs/py3/bin/python

from matching_functions import *
import glob, time, json, sqlite3, pickle, sys
from mako.template import Template
from collections import Counter

EEBO_SHINGLE_FOLDER = '/home/spenteco/0/eebo_shingled/'
METADATA_FILE = 'metadata/EEBO_metadata.tsv'
OUTPUT_FOLDER = 'all_to_all_html_outputs/'
RESULTS_PICKLE_FOLDER = 'text_reuse_pickle_outputs/'
#SQLITE3_DATABASE = '/ssd_data/shingles.sqlite3'
SQLITE3_DATABASE = '/data/shingles.sqlite3'

metadata = load_metadata(METADATA_FILE)

conn = sqlite3.connect(SQLITE3_DATABASE)
c = conn.cursor()

MAX_GAP_ALLOWED = 5
MIN_MATCH_LENGTH = 6

shingles_hash_time = {'n': 0, 'time': 0.0}
shingles_to_matches_time = {'n': 0, 'time': 0.0}
merged_matches_time = {'n': 0, 'time': 0.0}
pickle_time = {'n': 0, 'time': 0.0}
final_results_time = {'n': 0, 'time': 0.0}

def actually_check_matches(from_tcp_id, file_a, from_shingles, to_tcp_id, to_shingles_list, debug=False):
    
    if len(to_shingles_list) == 1:
        return None

    start_time = time.time()
    
    to_shingles = {}
    for s in to_shingles_list:
        to_shingles[s[1]] = s[2]
                    
    shingles_hash_time['n'] += 1
    shingles_hash_time['time'] += (time.time() - start_time)

    start_time = time.time()
        
    matches = []
    
    for k in to_shingles.keys():
        if k in from_shingles:
            for v_a in from_shingles[k]:
                for v_b in to_shingles[k]:
                    matches.append([v_a, v_b])
                    
    shingles_to_matches_time['n'] += 1
    shingles_to_matches_time['time'] += (time.time() - start_time)

    start_time = time.time()
                    
    merged_matches = merge_matches(matches, MAX_GAP_ALLOWED, MIN_MATCH_LENGTH)
                    
    merged_matches_time['n'] += 1
    merged_matches_time['time'] += (time.time() - start_time)
    
    final_results = None
    
    if len(merged_matches) > 0:

        start_time = time.time()
        
        file_b = None
        if debug == True:
            file_b = load_pickle_file(EEBO_SHINGLE_FOLDER + to_tcp_id + '.pickle')
                    
        pickle_time['n'] += 1
        pickle_time['time'] += (time.time() - start_time)

        start_time = time.time()
        
        final_results = make_final_results(merged_matches, file_a, file_b, 
                                           debug=debug, return_match_offsets=True)
                    
        final_results_time['n'] += 1
        final_results_time['time'] += (time.time() - start_time)
        
    return final_results

def get_metadata(tcp_id):
    
    author = 'METADATA ERROR'
    title = 'METADATA ERROR'
    year = 'MDER'

    try:

        author = metadata[tcp_id]['author']
        title = metadata[tcp_id]['title']
        year = metadata[tcp_id]['year']

    except KeyError:
        print('ERROR -- metadata?', tcp_id)

    return author, title, year
        
def find_text_reuse(from_tcp_id):
    
    #start_time = time.time()
    
    t = Template(filename='matching_results_template.html')
    
    from_author = metadata[from_tcp_id]['author']
    from_title = metadata[from_tcp_id]['title']
    from_year = metadata[from_tcp_id]['year']
    
    from_file = load_pickle_file(EEBO_SHINGLE_FOLDER + from_tcp_id + '.pickle')
    
    start_time = time.time()
    
    possible_matches = []
    
    for row in c.execute('select b.tcp_id, b.shingle, b.offsets from shingles a, shingles b ' + \
                         'where a.tcp_id = ? and b.tcp_id <> ? and a.shingle = b.shingle ',
                             (from_tcp_id, from_tcp_id,)):
        possible_matches.append([row[0], row[1], json.loads(row[2])])
                
    possible_matches.sort()
        
    print(from_tcp_id, len(from_file['shingles']), len(possible_matches))
    print('\t', 'A', (time.time() - start_time))
    
    all_results = []
    n_actually_check_matches = 0
    
    to_shingles = []
    last_key = None
    
    for m in possible_matches:
        if last_key != None and m[0] != last_key:
            
            n_actually_check_matches += 1
            
            check_result = actually_check_matches(from_tcp_id, from_file, from_file['shingles'], 
                                   last_key, to_shingles)
            
            if check_result != None:
                to_author, to_title, to_year = get_metadata(last_key)
                all_results.append([[last_key, to_author, to_title, to_year], check_result])
            
            to_shingles = []
            
        last_key = m[0]
        to_shingles.append(m)
        
    n_actually_check_matches += 1
    check_result = actually_check_matches(from_tcp_id, from_file, from_file['shingles'], 
                                           last_key, to_shingles)
    
    if check_result != None:
        to_author, to_title, to_year = get_metadata(last_key)
        all_results.append([[last_key, to_author, to_title, to_year], check_result])
        
    print('\t', 'B', (time.time() - start_time), 'n_actually_check_matches', n_actually_check_matches,
            'len(all_results)', len(all_results))
        
    if len(all_results) > 0:
        
        from_author, from_title, from_year = get_metadata(from_tcp_id)

        f = open(RESULTS_PICKLE_FOLDER + from_tcp_id + '.pickle', 'wb')
        pickle.dump([from_tcp_id, from_year, from_author, from_title, all_results], f)           
        f.close()
        
        build_match_report(from_tcp_id, EEBO_SHINGLE_FOLDER, RESULTS_PICKLE_FOLDER, OUTPUT_FOLDER)
        
        print('\t', 'C', (time.time() - start_time))
        

    print()
    print('\t\t', 'shingles_hash_time', shingles_hash_time)
    print('\t\t', 'shingles_to_matches_time', shingles_to_matches_time)
    print('\t\t', 'merged_matches_time', merged_matches_time)
    print('\t\t', '(no) pickle_time', pickle_time)
    print('\t\t', 'final_results_time', final_results_time)
    print()
    
    stop_time = time.time()
    
    print(from_tcp_id, 'done!', (stop_time - start_time), end='\n\n')

# ------------------------------------------------------------------------------------------------------

if __name__== "__main__":

    tcp_id = sys.argv[1]
    
    print()
    print(tcp_id, metadata[tcp_id], end='\n\n')

    find_text_reuse(tcp_id)
