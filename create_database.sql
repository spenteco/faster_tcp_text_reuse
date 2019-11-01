CREATE TABLE shingles (shingle TEXT NOT NULL, tcp_id TEXT NOT NULL, offsets TEXT NOT NULL);
.separator "	"
.import /home/spenteco/0/temp/shingle_data.0.txt shingles
.import /home/spenteco/0/temp/shingle_data.1.txt shingles
.import /home/spenteco/0/temp/shingle_data.2.txt shingles
.import /home/spenteco/0/temp/shingle_data.3.txt shingles
.import /home/spenteco/0/temp/shingle_data.4.txt shingles
.import /home/spenteco/0/temp/shingle_data.5.txt shingles
CREATE INDEX shingles_0 ON shingles(shingle);
CREATE INDEX shingles_1 ON shingles(tcp_id);
CREATE INDEX shingles_2 ON shingles(tcp_id, shingle);

