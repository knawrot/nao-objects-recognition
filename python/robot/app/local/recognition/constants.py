# GESTURE
MIN_HAND_AREA = 3200
OPEN_PALM_SOLIDITY_UPPER_BOUNDARY = 0.6
FIST_SOLIDITY_LOWER_BOUNDARY = 0.7
SKIN_LOWER_BOUNDARY = (0,16,39)
SKIN_UPPER_BOUNDARY = (20,78,255)

# TEXT
# Note: letters in paragraph are supposed to have similiar height/width ratio and occupy same area (i.e. have roughly equal size)
MIN_RATIO_OF_SIMILIAR_OBJECTS = 0.65
MIN_AREA_OF_SIMILIAR_OBJECTS = 0.5
MIN_CONTOURS_DETECTED = 100

# PHONE
# Note: to recognize a phone we use a constant defining minimum number of objects (icons, letters etc) for its screen
MIN_RATIO_OF_SCREEN = 0.7
MIN_NUM_OF_CONTOURS = 10
BRIGHT_OBJECTS_THRESHOLD = 200

# COLOR
COLOR_LOWER_BOUNDARY = (129,120,14)
COLOR_UPPER_BOUNDARY = (180,203,120)