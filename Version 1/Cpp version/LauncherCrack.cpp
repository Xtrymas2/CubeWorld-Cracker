#include <iostream>
#include <fstream>
using namespace std;

int get_file_size(string filename) {
  FILE * p_file = NULL;
  p_file = fopen(filename.c_str(), "rb");
  fseek(p_file, 0, SEEK_END);
  int size = ftell(p_file);
  fclose(p_file);
  return size;
}

int main()
{
    cout << "EXAMPLE: C:\\Program Files (x86)\\Cube World\\CubeLauncher.exe\nEnter path to launcher: ";
    string launchern;
    getline(cin, launchern);

    ifstream launcherh(launchern.c_str(), ios_base:: in | ios_base::binary);

    if(!launcherh){
        cout << "Unable to open " << launchern;
        cin;
        return 1;
    }

    int launcherSize = get_file_size(launchern);
    if (launcherSize != 163840){
        cout << "This is not the latest version of the launcher.\n";
        cout << "You can download it from:\n";
        cout << "https://d1bcl7tdsf48aa.cloudfront.net/download/CubeSetup3.exe";
        cin;
        return 1;
    }

    int pos = 0;
    char * launcherc =  new char[launcherSize];
    while (pos < launcherSize){
        launcherh.get(launcherc[pos]);
        pos++;
    }
    launcherh.close();

    string outfilename = "CubeLauncher_patched.exe";
    ofstream outfileh(outfilename.c_str(), ios_base::out | ios_base::binary);
    if (!outfileh){
        cout << "Unable to open " << outfilename;
        cin;
        return 1;
    }

    launcherc[0x14B46] = 0xEB; //switch jnz to jmp

    outfileh.write((char *) launcherc, pos);
    outfileh.close();

    cout << outfilename << " has been created";

    return 0;
}
