/PROG  ZIMG_ORIGIN
/ATTR
OWNER		= MNEDITOR;
COMMENT		= "";
PROG_SIZE	= 615;
CREATE		= DATE 21-11-30  TIME 11:15:30;
MODIFIED	= DATE 21-11-30  TIME 11:56:46;
FILE_NAME	= ;
VERSION		= 0;
LINE_COUNT	= 3;
MEMORY_SIZE	= 975;
PROTECT		= READ_WRITE;
TCD:  STACK_SIZE	= 0,
      TASK_PRIORITY	= 50,
      TIME_SLICE	= 0,
      BUSY_LAMP_OFF	= 0,
      ABORT_REQUEST	= 0,
      PAUSE_REQUEST	= 0;
DEFAULT_GROUP	= 1,*,*,*,*;
CONTROL_CODE	= 00000000 00000000;
/APPL
/MN
   1:J P[1:BoardtopLCornr] 100% CNT100    ;
   2:J P[2:littleFurtherLet] 100% CNT100    ;
   3:J P[3:MaxAchaiveableLt] 100% CNT100    ;
/POS
P[1:"BoardtopLCornr"]{
   GP1:
	UF : 9, UT : 4,		CONFIG : 'N U T, 0, 0, 0',
	X =   329.223  mm,	Y =   -62.318  mm,	Z =   -37.317  mm,
	W =   179.844 deg,	P =     -.746 deg,	R =     1.599 deg
};
P[2:"littleFurtherLet"]{
   GP1:
	UF : 9, UT : 4,		CONFIG : 'N U T, 0, 0, 0',
	X =   326.988  mm,	Y =   -63.718  mm,	Z =   -36.501  mm,
	W =   179.847 deg,	P =     -.751 deg,	R =     1.602 deg
};
P[3:"MaxAchaiveableLt"]{
   GP1:
	UF : 9, UT : 4,		CONFIG : 'N U T, 0, 0, 0',
	X =   325.415  mm,	Y =   -88.117  mm,	Z =   -41.069  mm,
	W =   179.490 deg,	P =      .405 deg,	R =    49.579 deg
};
/END
