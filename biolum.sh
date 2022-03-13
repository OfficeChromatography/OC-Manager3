#script to take sequences of bioluminescent images

echo "*****************************************************************************"
echo "Setup for a sequence taking images of luminescent bacteria on an HPTLC plate."
echo "*****************************************************************************"
echo ""
echo "Enter exposure time (s):"
read SHUTSPEED
echo "Enter the number of images you want to take:"
read Z

PT=$(($SHUTSPEED / 8)) #time in min needed to capture one image

if [ $Z -gt 1 ]; then
   echo "Enter the waiting time (>= $PT, min) between capturing the images:"
   read TL    #trigger interval in min
else
   TL=$PT
fi

TL1=$[$TL-$PT]
TL2=$[$TL1*60]  #minutes into seconds, this value is used for the sleep time in function IMAGE

echo "Enter the stem name of your images files:" 
read stem
NULL=0

SHUTSPEED1=$[$SHUTSPEED*1000*1000] #transformation in µs, used for raspistill

#calculation the total time for the image sequence
TIME=$[$PT*$Z+($TL*($Z-1))]   #total time in min

BIO=bioluminescence
if [[ ! -d "$BIO" ]]
then
   mkdir $BIO
fi
FOLDER=$(date +%Y%m%d_%H%M%S)
mkdir $BIO/$FOLDER 
echo ""
echo "The images are saved in a new folder named $(pwd)/$BIO/$FOLDER"
echo ""
echo "The total time to take the images is about $TIME min."

echo ""
#Function IMAGE
IMAGE()
{  
   date +”%H:%M:%S”
   for i in `seq 1 $Z`
      do
      echo "capturing image $i"
	  raspistill -o $(pwd)/$BIO/$FOLDER/$stem$i.jpg -ISO 800 -drc low -q 100 -sa 20 -awb horizon -ss $SHUTSPEED1 -w 2028 -h 1520 -n &
      pid=$!
	  #echo "pid $pid"
	  wait $pid
	  wmctrl -c $stem
	  xdg-open $(pwd)/$BIO/$FOLDER/$stem$i.jpg   #opens the image in the image viewer
	  if [ $i -lt $Z ]; then
	     echo "waiting $TL min"
	     sleep $TL2 #in seconds
	  else
	     sleep $NULL
	  fi
   done
   date +”%H:%M:%S”
}
echo "Are you ready to start (y)? Press any other key to skip."
read answer
echo ""
if [ "$answer" == "y" ]
  then	#all other inputs go to else
  IMAGE
  $(pwd)/distort.py --file-format jpg --source-folder $(pwd)/$BIO/$FOLDER --output-folder $(pwd)/$BIO/$FOLDER/corrected/
  echo "Job done!"
else
  echo "The process was skipped!"
fi
