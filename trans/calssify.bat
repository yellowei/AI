opencv_traincascade.exe -data INRIAPerson -vec pos\pos.vec -bg neg\neg.dat -numPos 2416 -numNeg 1268 -numStages 10 -w 96 -h 160 -minHitRate 0.9999 -maxFalseAlarmRate 0.5 -featureType HOG
pause