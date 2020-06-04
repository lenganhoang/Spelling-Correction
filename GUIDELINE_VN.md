# Hướng dẫn submit cho cuộc thi AI Hackathon 2019.
## 0. Giới thiệu
AI Hackathon 2019 là một cuộc thi nhằm tìm kiếm tài năng, đồng thời là sân chơi giao lưu giữa những người trẻ có chung đam mê trong lĩnh vực AI-ML.

Để có thể ghi tên mình trên bảng xếp hạng của cuộc thi, sau đây là phương pháp submit kết quả dành cho các đội thi.

## 1. Phương pháp submit của cuộc thi
Trong cuộc thi này, các đội sẽ đóng gói mô hình AI-ML của mình vào trong một file Docker Image, upload và chia sẻ file này với ban tổ chức cuộc thi.

Ban tổ chức cuộc thi sẽ chạy file Docker Image của người tham dự gửi trên dữ liệu test của cuộc thi. Kết quả sẽ được công bố sau khi chạy file Docker Image thành công.

## 2. Hướng dẫn thiết lập môi trường Docker CE (Community Edition).

Sau đây là đường dẫn đến các trang tải và hướng dẫn cài Docker cũng như cơ bản về cách sử dụng các lệnh trong Docker.

Những hệ điều hành không được đề cập, người tham dự tự tìm hướng dẫn cài đặt trên trang chủ của Docker https://docs.docker.com/.

### 2.1 Dành cho người dùng Windows
- Tải ứng dụng Docker Desktop for Windows tại: https://hub.docker.com/editions/community/docker-ce-desktop-windows
- Làm theo hướng dẫn tại trang https://docs.docker.com/docker-for-windows/install/ để cài và khởi chạy Docker.
- Bắt đầu làm quen với Docker tại trang: https://docs.docker.com/docker-for-windows/

### 2.2 Dành cho người dùng Mac
- Tải ứng dụng Docker Desktop for Mac tại: https://hub.docker.com/editions/community/docker-ce-desktop-mac
- Làm theo hướng dẫn tại trang https://docs.docker.com/docker-for-mac/install/ để cài và khởi chạy Docker.
- Bắt đầu làm quen với Docker tại trang: https://docs.docker.com/docker-for-mac/

### 2.3 Dành cho người dùng Linux (Ubuntu):
- Làm theo hướng dẫn tại trang https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04 để cài và khởi chạy Docker.

Sau khi cài đặt và khởi chạy Docker, đảm bảo rằng bạn có thể truy cập vào cửa sổ dòng lệnh (terminal) trên hệ điều hành và chạy lệnh sau thành công:
```
docker --version
```

Nếu không có vấn đề gì, dòng lệnh trên sẽ hiện kết quả có dạng:
```
Docker version 18.09.7, build 2d0083d
```
Số phiên bản và mã build của ứng dụng Docker có thể khác nhau.

Bạn nên cài phiên bản ổn định (stable) và mới nhất hiện nay của Docker để đảm bảo Docker Image bạn tạo ra chạy được trong môi trường của ban tổ chức khi tính điểm cho giải pháp của bạn.

## 3. Hướng dẫn tạo Docker image chứa chương trình tính toán cần cho submit.

Sau đây là hướng dẫn tạo Docker image chứa ứng dụng của người tham dự nhằm phục vụ cho mục đích tính điểm.

### 3.1 Cách sử dụng template.
Repo này là một template (khuôn mẫu) nhằm tạo Docker Image tương thích với mục đích submit của ban tổ chức.


#### 3.1.1 Dockerfile
File `Dockerfile` chứa các chỉ thị cho chương trình Docker cách tạo một Docker Image.

Image được sử dụng làm cơ sở để tạo Docker image mới mặc định là image `python` phiên bản `3.6-slim-buster`.

Mặc định docker image tạo ra sẽ chứa python phiên bản 3.6 và chạy file `main.py`.

Nếu bạn không sử dụng `python` trong giải pháp của mình, bạn có thể cân nhắc thay đổi Image cơ sở sang image tổng quát hơn như `ubuntu:18.04`

#### 3.1.2 requirements.txt
File `requirements.txt` chứa các thư viện cần thiết để chạy file `main.py`.
Ví dụ như trong file `requirements.txt` mặc định chứa thư viện `pandas` phiên bản `0.25.3`.

Các thư viện này sẽ được cài khi Docker image được xây dựng thông qua lệnh ```RUN pip3 install -r /app/requirements.txt``` trong file `Dockerfile`.

#### 3.1.3 main.py
Đây là file chương trình chính, sẽ được chạy khi gõ lệnh `docker run`.

Chương trình này nhận 2 tham số đầu vào `input_file` ứng với file đầu vào chứa các câu chưa được sửa lỗi. `output_file` ứng với file đầu ra chứa các câu đã được sửa lỗi.

Người tham dự nên giữ nguyên 2 tham số này vì đây là giao diện để ban tổ chức chạy Docker image của bạn.

Nội dung khác trong file main.py hoàn toàn có thể thay đổi cho phù hợp với giải pháp của người tham dự.

#### 3.1.4 Makefile
File `Makefile` chứa một số những cụm câu lệnh hữu ích.
Cách sử dụng file Makefile này là gõ lệnh:
```
make <command>
```
trong đó command là tên của các cụm câu lệnh. Ví dụ cụm câu lệnh `build`:
```
build:
	docker build -t python-inference:0.0.2 .
```
sẽ khiến chương trình `docker` xây dựng Docker image mới dựa trên mô tả trong file `Dockerfile` đề cập bên trên. Cách chạy cụm lệnh này là `make run`.

> NOTE: Lưu ý rằng khi chạy các lệnh này, cửa sổ Terminal của các bạn phải ở thư mục hiện tại, tức thư mục chứa các file `Makefile` và `Dockerfile`.

### 3.2 Các bước trong tạo, kiểm tra và sử dụng Docker image.

#### 3.2.1 Tạo Docker image.
Ta sử dụng lệnh:
```
docker build -t python-inference:0.0.2 .
```
để build (xây dựng) một Docker Image chứa các file cần thiết (code, mô hình, thư viện) để chạy ứng dụng `main.py` với file đầu vào và đầu ra mong muốn.

Ở đây `python-inference` là tên của Docker image, `0.0.2` là phiên bản của Docker image. Nếu bạn không cung cấp phiên bản của Docker image bằng cách điền vào sau dấu `:` thì phiên bản mặc định của Docker sẽ là `latest`.

Nếu không có lỗi gì xảy ra, `docker` sẽ build image và lưu trữ vào bên trong ứng dụng.
Để kiểm tra, bạn có thể sử dụng lệnh:
```
docker image inspect python-inference:0.0.2
```

#### 3.2.2 Kiểm tra Docker image chạy được.
Ta sử dụng lệnh:
```
docker run --rm python-inference:0.0.2 --help
```
Nếu Docker image hoạt động, kết quả output của terminal sẽ hiển thị hướng dẫn sử dụng file `main.py`, ví dụ như sau:
```
usage: main.py [-h] input_file output_file

Correcting texts in an input file

positional arguments:
  input_file   Path to the input text file
  output_file  Path to the output corrected text file

optional arguments:
  -h, --help   show this help message and exit
```

> NOTE: Lệnh `docker run` sẽ tạo một container từ image đầu vào. Container giống như một máy ảo (virtual machine), nhưng nhẹ hơn nhiều.

> NOTE: Image giống như bản mẫu để tạo máy ảo với các chương trình đã được cài sẵn (ở đây là `main.py` với thư viện `pandas` đi kèm), chỉ cần tạo container là có thể chạy được chương trình bên trong (ở dòng lệnh bên trên là chạy file `main.py` với tham số  `--help` để tìm hiểu cách chạy chương trình).

#### 3.2.3 Chạy Docker image với file input.txt và output.txt
Ta sử dụng câu lệnh:
```
docker run --rm -v /home/user/input.txt:/tmp/input.txt -v /home/user/output.txt:/tmp/output.txt python-inference:0.0.2 /tmp/input.txt /tmp/output.txt
```

Trong câu lệnh này, phần tham số  `-v /home/user/input.txt:/tmp/input.txt` được sử dụng để **mount** (**một dạng kết nối - shortcut hay symbolic link**) một file ở máy host (ở đây là file `/home/user/input.txt`) với một file ảo ở trong Docker container (ở đây là `/tmp/input.txt`).

Phần tham số  `-v /home/user/output.txt:/tmp/output.txt` cũng tương tự, dùng để mount file `/home/user/output.txt` với một file ảo `/tmp/output.txt`.

Hai file ảo này sau đó được sử dụng trong phần còn lại của câu lệnh, trở thành `input_file` và `output_file` khi chạy Docker image.

Người tham dự hoàn toàn có thể thay đổi đường dẫn của `output.txt` và `input.txt` cho phù hợp 

> NOTE: `input.txt` là file chứa dữ liệu đầu vào, trong đó mỗi dòng là một câu có lỗi cần sửa.
> `output.txt` là file chứa dữ liệu đầu ra, mỗi dòng trong file này có nội dung giống với dòng tương ứng trong file `input.txt`, nhưng đã được sửa lỗi.

> NOTE: Tham số  `--rm` được sử dụng để chỉ thị cho `docker` xóa container ngay sau khi chương trình bên trong container kết thúc.

#### 3.2.4 Lưu Docker image thành file để chia sẻ.
Ta sử dụng câu lệnh:
```
docker save -o python-inference:0.0.2.tar python-inference:0.0.2
```
để xuất Docker image đã được tạo thành công ra thành 1 file image có thể chuyển sang máy khác và sử dụng chương trình `docker` để tái tạo lại Docker image này.

Tham số  `-o python-inference:0.0.2.tar` cấu hình đường dẫn đến file image kết quả.

> NOTE: File docker image này sẽ được sử dụng như kết quả để tính điểm cho các đội thi.
Người tham dự cần lưu lại file này và gửi tới ban tổ chức thông qua hướng dẫn ở phần [4 - Hướng dẫn submit Docker image.](#4.-Hướng-dẫn-submit-Docker-image.).
#### 3.2.5 Tái tạo Docker image từ file image.
Ta sử dụng câu lệnh:
```
docker load -i python-inference:0.0.2.tar
```
để tái tạo lại Docker image mà không cần phải build từ Dockerfile.

## 4. Hướng dẫn submit Docker image.
Người tham dự sẽ gửi email với file Docker image được đính kèm (nếu kích thước file lớn hơn kích thước tối đa của email, người tham dự upload file lên google drive và chia sẻ quyền truy cập với email của ban tổ chức: aihackathon@icomm.vn).

**Người gửi email là phải người đại diện của nhóm**. 

Email cần có tiêu đề dạng: `AI_HACKATHON_SUBMIT_{Tên đại diện nhóm}_{Ngày}_{Tháng}_{Năm}`, gửi vào địa chỉ email: aihackathon@icomm.vn. 

**Khi gửi email phải cc (carbon copy) đầy đủ các thành viên khác trong nhóm**.