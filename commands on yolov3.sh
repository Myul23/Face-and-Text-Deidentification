# train
python train.py --weights yolov3.pt --batch-size 8 --data custom.yaml --workers 8 --project runs

# inference
python val.py --weights yolov3.pt --data custom-test.yaml --save-txt --task test --verbose
python val.py --weights best.pt --data cusom-test.yaml --half --task test

# predict
python detect.py --weights best.pt --source test/images/ --hide-labels
python detect.py --weights best.pt --source test/images/ --save-txt --nosave
