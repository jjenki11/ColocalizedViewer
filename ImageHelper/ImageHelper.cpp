#include "stdio.h"
#include <linux/stat.h>
#include <sys/stat.h>
#include <Magick++.h>
#include <iostream> 
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <iterator>
using namespace std; 
using namespace Magick; 


bool GetImageSize(string fn, int *x,int *y)
{
    FILE *f=fopen(fn.c_str(),"rb");
    if (f==0) return false;
    fseek(f,0,SEEK_END);
    long len=ftell(f);
    fseek(f,0,SEEK_SET);
    if (len<24) {
        fclose(f);
        return false;
        }
    cout << fn << endl;
  // Strategy:
  // reading GIF dimensions requires the first 10 bytes of the file
  // reading PNG dimensions requires the first 24 bytes of the file
  // reading JPEG dimensions requires scanning through jpeg chunks
  // In all formats, the file is at least 24 bytes big, so we'll read that always
  unsigned char buf[24]; fread(buf,1,24,f);

  // For JPEGs, we need to read the first 12 bytes of each chunk.
  // We'll read those 12 bytes at buf+2...buf+14, i.e. overwriting the existing buf.
  if (buf[0]==0xFF && buf[1]==0xD8 && buf[2]==0xFF && buf[3]==0xE0 && buf[6]=='J' && buf[7]=='F' && buf[8]=='I' && buf[9]=='F')
  { long pos=2;
    while (buf[2]==0xFF)
    { if (buf[3]==0xC0 || buf[3]==0xC1 || buf[3]==0xC2 || buf[3]==0xC3 || buf[3]==0xC9 || buf[3]==0xCA || buf[3]==0xCB) break;
      pos += 2+(buf[4]<<8)+buf[5];
      if (pos+12>len) break;
      fseek(f,pos,SEEK_SET); fread(buf+2,1,12,f);
    }
  }

  fclose(f);

  // JPEG: (first two bytes of buf are first two bytes of the jpeg file; rest of buf is the DCT frame
  if (buf[0]==0xFF && buf[1]==0xD8 && buf[2]==0xFF)
  { *y = (buf[7]<<8) + buf[8];
    *x = (buf[9]<<8) + buf[10];
    //cout << *x << endl;
    return true;
  }

  // GIF: first three bytes say "GIF", next three give version number. Then dimensions
  if (buf[0]=='G' && buf[1]=='I' && buf[2]=='F')
  { *x = buf[6] + (buf[7]<<8);
    *y = buf[8] + (buf[9]<<8);
    return true;
  }

  // PNG: the first frame is by definition an IHDR frame, which gives dimensions
  if ( buf[0]==0x89 && buf[1]=='P' && buf[2]=='N' && buf[3]=='G' && buf[4]==0x0D && buf[5]==0x0A && buf[6]==0x1A && buf[7]==0x0A
    && buf[12]=='I' && buf[13]=='H' && buf[14]=='D' && buf[15]=='R')
  { *x = (buf[16]<<24) + (buf[17]<<16) + (buf[18]<<8) + (buf[19]<<0);
    *y = (buf[20]<<24) + (buf[21]<<16) + (buf[22]<<8) + (buf[23]<<0);
    return true;
  }

  return false;
}


template<typename Out>
void split(const std::string &s, char delim, Out result) {
    std::stringstream ss;
    ss.str(s);
    std::string item;
    while (std::getline(ss, item, delim)) {
        *(result++) = item;
    }
}


std::vector<std::string> split(const std::string &s, char delim) {
    std::vector<std::string> elems;
    split(s, delim, std::back_inserter(elems));
    return elems;
}


int main(int argc,char **argv) 
{ 
  InitializeMagick(*argv);

  // Construct the image object. Separating image construction from the 
  // the read operation ensures that a failure to read the image file 
  // doesn't render the image object useless. 
  if(argc < 6){
    cout << "please input the correct # of args." << endl;
    exit(0);
  }
  string fname = argv[1];
  
  int ul_x = atoi(argv[2]);
  int ul_y = atoi(argv[3]);
  
  int width = atoi(argv[4]);
  int height = atoi(argv[5]);
  
  
  cout << "Filename -> " << fname << endl;
  cout << "UL -> (" << ul_x << ", " << ul_y << ")" << endl;
  cout << "w/h -> (" << width << ", " << height << ")" << endl;
  Image image;
  try { 
    // Read a file into image object 
    image.read( fname );
    
    std::vector<std::string> the_path = split(fname, '/');
    
    std::string abc;
    
    for(int i = 0; i < the_path.size()-1; i++)
    {
        abc = abc+the_path[i] + "/";
    }
    
    cout << "THE DIRECTORY THIS FILE LIVES IN -> " << abc << endl;
    
    int the_x  = 0;
    int the_y = 0;
    
    bool didRun = false;
    
    didRun = GetImageSize(fname, &the_x, &the_y);
    
    cout << "IMAGE WIDTH/HEIGHT ->     " << the_x << "/" << the_y << endl;
    
    if(the_x < (ul_x+width)){
        cout << "Bad image query in the width." << endl;
        exit(0);
    }
    
    if(the_y < (ul_y+height)){
        cout << "Bad image query in the height." << endl;
        exit(0);
    }


    // Crop the image to specified size (width, height, xOffset, yOffset)
    image.crop( Geometry(width, height, ul_x, ul_y) );

    // Write the image to a file 
    image.write( abc+"crop_result.jpg" ); 
    /*
    ofstream myfile;
    myfile.open (abc+"test.txt");
    myfile << "Writing this to a file.\n";
    myfile.close();
    */
    cout << "DONE with crop." << endl;
  } 
  catch( Exception &error_ ) 
    { 
      cout << "Caught exception: " << error_.what() << endl; 
      return 1; 
    } 
  return 0; 
}
