# MDCT
Đây là repo cho bài tập lớn của môn Truyền thông đa phương tiện.

Các file audio để test nằm trong thư mục "audios". Sử dụng MDCT để nén các file này.

Các file sau khi nén bởi DCT và MDCT nằm trong folder outputs, trong thư mục tương ứng với cách nén.

# Setup môi trường để lập trình
Chạy `pip install -r requirements.txt` để cài các dependencies cần dùng cho project này.

# Cách sử dụng
Chạy `python wavmdct.py -h` để xem danh sách các options
```bash
$ python wavmdct.py -h
usage: wavmdct.py [-h] (-d | -m) -s SAMPLE_PER_FRAME -c COMPRESS_RATIO file

Compress WAV audio files with MDCT

positional arguments:
  file                  input file location

optional arguments:
  -h, --help            show this help message and exit
  -d, --dct             use DCT on the input audio file
  -m, --mdct            use MDCT on the input audio file
  -s SAMPLE_PER_FRAME, --sample-per-frame SAMPLE_PER_FRAME
                        number of samples per frame
  -c COMPRESS_RATIO, --compress-ratio COMPRESS_RATIO
                        compress ratio
```
