#cs ----------------------------------------------------------------------------

 AutoIt Version: 3.3.14.2
 Author:         myName

 Script Function:
	Template AutoIt script.

#ce ----------------------------------------------------------------------------

; Script Start - Add your code below here
ControlFocus("打开","","Edit1")
WinWait("[CLASS:#32770]","",5)
Sleep(1000)
ControlSetText("打开","","Edit1",$CmdLine[1])
Sleep(1000)
ControlClick("打开","","Button1")
Sleep(1000)