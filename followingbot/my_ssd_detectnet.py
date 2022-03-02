# 1. jetson-infernece 라이브러리 임포트
import jetson.inference
import jetson.utils

# 2. 파이썬 인자 파서 임포트
import argparse
import sys
# kate.brighteyes@gmail.com
# 20210720

# 실행 인자 파서 처리
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 
parser.add_argument("--input-blob", type=str, default="input_0", help="input-blob")
parser.add_argument("--output-cvg", type=str, default="scores", help="output-cvg")
parser.add_argument("--output-bbox", type=str, default="boxes", help="output-bbox")

is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# 객체인식 모델 로딩
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

# 입력 소스와 결과물 소스 지정, 여기서 입력은 카메라, 결과물은 화면으로 지정함.
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+is_headless)

# 사용자가 끝낼때 까지 실행함
while True:
	# 다음 이미지 캡처
	img = input.Capture()

	# 이미지에서 객체를 인식합니다.
	detections = net.Detect(img, overlay=opt.overlay)

	# 인식한 객체를 화면에 보여줍니다.
	print("detected {:d} objects in image".format(len(detections)))

	for detection in detections:
		print(detection)

	# 바운딩박스가 그려진 이미지를 화면에 그려줍니다.
	output.Render(img)

	# 타이틀 바를 갱신해줍니다.
	output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))

	# 추론 성능을 표시해줍니다. 
	net.PrintProfilerTimes()

	# 입력이나 결과물 스트리밍이 끝나면 실행을 종료합니다.
	if not input.IsStreaming() or not output.IsStreaming():
		break
