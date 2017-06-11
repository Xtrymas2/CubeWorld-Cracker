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
    cout << "EXAMPLE: C:\\Program Files (x86)\\Cube World\\Cube.exe\nEnter path to Cube.exe: ";
    string cuben;
    getline(cin, cuben);

    ifstream cubeh(cuben.c_str(), ios_base:: in | ios_base::binary);

    if(!cubeh){
        cout << "Unable to open " << cuben;
        cin;
        return 1;
    }

    int cubeSize = get_file_size(cuben);
    if (cubeSize != 3885568){
        cout << "This is not the latest version of Cube World.\n";
        cout << "If you are trying to use this on an older version, try the python version of this program.\n";
        cout << "The python script should work on any version.\n";
        //I'm mentally challenged and I wish I was taught C++ in college instead of Python
        cin;
        return 1;
    }

    char * cubec =  new char[cubeSize];
    for (int pos = 0; pos < cubeSize; pos++){
        cubeh.get(cubec[pos]);
    }
    cubeh.close();

    string outfilename = "Cube_patched.exe";
    ofstream outfileh(outfilename.c_str(), ios_base::out | ios_base::binary);
    if (!outfileh){
        cout << "Unable to open " << outfilename;
        cin;
        return 1;
    }

    for(int i = 0x5A18D; i < 0x5A193; i++){
        cubec[i]=0x90;//nop some bytes and stuff to make things good
    }

    outfileh.write((char *) cubec, cubeSize);
    outfileh.close();

    cout << outfilename << " has been created";
    cin;

    return 0;
}
