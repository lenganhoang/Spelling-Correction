# Build the image.
build:
	docker build -t python-inference:0.0.2 .

# Get help of how to run command inside the built image.
help:
	docker run --rm python-inference:0.0.2 --help

# Example of run processing an input file and save result to ANOTHER output file.
# Make sure that the input file (input.txt) and output file (output.txt) exist, the output file have to be a blank text file.
run:
	docker run --rm -v /home/user/input.txt:/tmp/input.txt -v /home/user/output.txt:/tmp/output.txt python-inference:0.0.2 /tmp/input.txt /tmp/output.txt

# Save the built image to compressed file for submission.
save:
	docker save -o python-inference:0.0.2.tar python-inference:0.0.2

# Load the compressed file to Docker image.
load:
	docker load -i python-inference:0.0.2.tar
