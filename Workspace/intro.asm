; http://www.math.sci.hiroshima-u.ac.jp/m-mat/MT/TINYMT/index.html
; stuff goes here

;1.1 - Reasons for using assembly code

;Assembly coding is not used as much today as previously. 
;However, there are still reasons for learning and using 
;assembly code. The main reasons are:

; 1.Educational reasons. 
;	- It is important to know how microprocessors and compilers work 
;		at the instruction level in order to be able to predict which coding 
;		techniques are most efficient, to understandhow various constructs in 
;		high level languages work, and to track hard-to-find errors.
;
; 2.Debugging and verifying.
;	- Looking at compiler-generated assembly code or the disassembly window
;		in a debugger is useful for finding errors and for checking how well a
;		compiler optimizes a particular piece of code.

; 3.Making compilers. 
;	- Understanding assembly coding techniques is necessary for making 
;		compilers, debuggers,and other development tools.
;
; 4.Embedded systems.
;	 - Small embedded systems have fewer resources than PC's and mainframes. 
;	 	Assembly programming can be necessary for optimizing code for speed or 
;	 	size in small embedded systems.
;
; 5.Hardware drivers and system code.
;	 - Accessing hardware, system control registers,etc. may sometimes be 
;	 	difficult or impossible with high level code.
;
; 6.Accessing instructions that are not accessible from high level language. 
;	- Certain assembly instructions have no high-level language equivalent.

;7.Self-modifying code.
;	- Self-modifying code is generally not profitable because it interferes
;		with efficient code caching. It may, however, be advantageous for 
;		example to include a small compiler in math programs where a 
;		user-defined function has to be calculated many times.
;
; 8.Optimizing code for size. 
;	- Storage space and memory is so cheap nowadays that it is not worth 
;		the effort to use assembly language for reducing code size. However
;		cache size is still such a critical resource that it may be useful 
;		in some cases to optimize a critical piece of code for size in order
;		to make it fit into the code cache.9.Optimizing code for speed. 
;		Modern C++ compilers generally optimize code quite well in most cases.
;		But there are still cases where compilers perform poorly and where
;		significant increases in speed can be achieved by careful
;		assembly programming. 

; 10.Function libraries. 
;	- The total benefit of optimizing code is higher in function libraries 
;		that are used by many programmers.
;
; 11.Making function libraries
;	- compatible with multiple compilers and operating systems. It is possible
;		to make library functions with multiple entries that are compatible 
;		with different compilers and different operating systems. 
;		This requires assembly programming.

;Here is a checklist of things to consider before you start programming:

;	- Never make the whole program in assembly. That is a waste of time.
;		Assembly code should be used only where speed is critical and where 
;		a significant improvement in speed can be obtained. Most of the program 
;		should be made in C or C++. These are the programming languages that are 
;		most easily combined with assembly code
;	
;	- If the purpose of using assembly is to make system code or use special 
;		instructions that are not available in standard C++ then you should 
;		isolate the part of the program that needs these instructions in a 
;		separate function or class with a well-definedfunctionality. 
;		Use intrinsic functionsinstead(see p. 33) if possible.
;	
;	- If the purpose of using assembly is to optimize for speed,then you have 
;		to identify the part of the program that consumes the most CPU time,
;		possibly with the use of a profiler. Check if the bottleneck is file 
;		access, memory access, CPU instructions, or something else, as
;		described in manual 1: "Optimizing software in C++". 
;		Isolate the critical part of the program into a function or class 
;		with a well-defined functionality.
;	
;	- If the purpose of using assembly is to make a function library then you 
;		should clearly define the functionality of the library. Decide whether 
;		to make a function library or a class library. Decide whether to use 
;		static linking (.lib in Windows, .a in Linux)
;		or dynamic linking (.dll in Windows, .so in Linux). 
;		Static linking is usually more efficient, 
;		but dynamic linking may be necessary if the library is called from 
;		other languages than C or C++. You may possibly make both a static 
;		and a dynamic link version of the library.
;	
;	- If the purpose of using assembly is to optimize an embedded application 
;		for size or speed,then find a development tool that supports both C/C++ 
;		and assembly and make as much as possible in C or C++
;==========================================================================
; BEGIN CODE SECTION
;==========================================================================
;Static Data Regions
;	- analogous to global variables
;
; Shall be preceded by the .DATA directive. 
;Following this directive
;	- DB
;	- DW
;	- DD 
;  can be used 
; to declare one, two, and four byte data locations, respectively. 
; Declared locations can be labeled with names for later reference — 
; this is similar to declaring variables by name, but abides by 
; some lower level rules. For example, locations declared in sequence 
; will be located in memory next to one another.

;Example declarations: 
 
.DATA
	DB 10 	; Declare a byte with no label, containing the value 10. Its location is var2 + 1.
byteone	DB 64  	; Declare a byte
                ; referred to as location var, containing the value 64.
bytetwo   DB ?	; Declare an uninitialized byte, referred to as location var2.
X 	DW ? 	; Declare a 2-byte uninitialized value, referred to as location X.
Y 	DD 30000; Declare a 4-byte value, referred to as location Y, initialized to 30000. 

; "call"
;	- used to call another function.   
;	- function can then return using "ret" 
;	- stores the return address to jump back to on the stack, 


mov edi,7 ; pass a function parameter
call randextract ; run the function below, until it does "ret"
add eax,1 ; modify returned value
ret


randextract: ; a function "declaration" in assembly
	mov eax,edi ; return our function's only argument
	ret