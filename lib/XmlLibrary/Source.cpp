/*
 * Facetracker 
 * @authors : Hamza & Godeleine & Quentin
 *
*/
#include <stdlib.h>
//#include <stdio.h>
#include <iostream>
//#include <string.h>
//#define _CRTDBG_MAP_ALLOC_
//#include <crtdbg.h>

//#include "tinyxml.h"
#include "../../Header/XmlParsing.h"

using namespace std;

/*
 * A la fin de ce main, le fichier DATAtest doit etre le m�me que DATAresult
 */

int main()
{
	DATA data("DATAtest.xml");

	//affiche data tout juste initialis�
	cout << "initialisation ..." << endl;
	cout << data.getNodeName() << endl;
	data.printDATAInfo();
	
	//On se d�place dans la deuxi�me node (url2)
	cout << "Testing moveIntoFolder" << endl;
	data.moveIntoFolder("url2");
	cout << data.getNodeName() << endl;
	data.printDATAInfo();
	data.moveIntoFolder("url3");

	//On r�cup�re la premi�re image du dossier url2 (image2)
	cout << "getting image2" << endl;
	data.moveIntoFolder("url2");
	data.setImageFromXml();
	data.image.printInfo();

	//On supprime l'image r�cup�r�e
	cout << "Testing deleteImageFromXml()" << endl;
	data.deleteImageFromXml();
	data.deleteImageFromXml();

	system("pause");

	//On se replace dans la node data url1 et on ajout l'image
	data.moveIntoFolder("url1");
	cout << "Testing addImageToXml()" << endl;
	data.addImageToXml();
#ifdef _WIN32
	system("pause");
#endif
	return 0;
}
