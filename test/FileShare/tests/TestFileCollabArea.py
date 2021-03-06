# ---------------------------------------------------------------------
#
# Copyright (c) 2012 University of Oxford
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, --INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
# ---------------------------------------------------------------------

# $Id: TestFileCollabArea.py 1047 2009-01-15 14:48:58Z graham $

#
# Unit testing for access to collab file area
#

import os
import sys
import httplib
import urllib2
import unittest
import subprocess

sys.path.append("../..")

from TestConfig import TestConfig

import TestCifsUtils
import TestHttpUtils

class TestFileCollabArea(unittest.TestCase):
        
    def setUp(self):
        return

    def tearDown(self):
        return

    def HTTP_redirect(self, opener, method, uri, data, content_type):
        TestHttpUtils.do_HTTP_redirect(opener, method, uri, data, content_type)
        return
    
    def cifsMountAs(self, userArea, userName, userPass):
        status= TestCifsUtils.do_cifsMount('collab/'+userArea, userName, userPass)
        if status != 8192:      
            self.assertEqual(status, 0, 'CIFS Mount failure')
        return status
    
    def cifsMount(self, userName, userPass):
        self.cifsMountAs(userName, userName, userPass)
        return

    def cifsUnmount(self):
        TestCifsUtils.do_cifsUnmount()
        return

    def cifsCreateFile(self, fileName, createFileContent):
        TestCifsUtils.do_cifsCreateFile(fileName, createFileContent)
        return createFileContent

    def cifsReadFile(self, fileName ):
        readFileContent = TestCifsUtils.do_cifsReadFile(fileName)
        return  readFileContent
    
    def cifsUpdateFile(self,fileName, updateFileContent):
        TestCifsUtils.do_cifsUpdateFile(fileName, updateFileContent)
        return updateFileContent
    
    def cifsDeleteFile(self,fileName):
        deleteMessage = TestCifsUtils.do_cifsDeleteFile(fileName)
        return  deleteMessage
    
    def httpAuthenticationHandler(self,userName, userPass):
        authhandler = TestHttpUtils.do_httpAuthenticationHandler(userName, userPass)
        return authhandler
    
    def httpCreateFileAs(self, areaName, userName, userPass, fileName, fileContent):
        createMessage = TestHttpUtils.do_httpCreateFile('collab/'+areaName, userName, userPass, fileName, fileContent)
        return createMessage
    
    def httpCreateFile(self, userName, userPass, fileName, fileContent):
        createMessage = self.httpCreateFileAs(userName, userName, userPass, fileName, fileContent)
        return createMessage
    
    def httpReadFileAs(self, areaName, userName, userPass,fileName):
        readFileContent = TestHttpUtils.do_httpReadFile( 'collab/'+areaName, userName, userPass,fileName)
        return readFileContent

    def httpReadFile(self, userName, userPass,fileName):
        readFileContent = self.httpReadFileAs(userName, userName, userPass,fileName)
        return readFileContent
      
    def httpUpdateFileAs(self, areaName, userName, userPass,fileName, updateFileContent):
        updateMessage = TestHttpUtils.do_httpUpdateFile('collab/'+areaName, userName, userPass,fileName, updateFileContent)
        return updateMessage
    
    def httpUpdateFile(self, userName, userPass,fileName, updateFileContent):
        updateMessage = self.httpUpdateFileAs(userName, userName, userPass,fileName, updateFileContent)
        return updateMessage
    
    def httpDeleteFileAs(self, areaName, userName, userPass,fileName):
        deleteMessage = TestHttpUtils.do_httpDeleteFile( 'collab/'+areaName, userName, userPass,fileName)
        return deleteMessage
    
    def httpDeleteFile(self, userName, userPass,fileName):
        deleteMessage = self.httpDeleteFileAs(userName, userName, userPass,fileName)
        return deleteMessage

    def testNull(self):
        assert (True), "True expected"
        return


    # Test User A's access permissions in his own collab area
    
    def testUserACreateCIFSUserAReadCIFS(self): 
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        createdFileContent = self.cifsCreateFile(fileName, fileContent)       
        readFileContent = self.cifsReadFile(fileName) 
        self.assertEqual(createdFileContent,readFileContent)    
        self.cifsUnmount()
        return

    def testUserACreateCIFSUserAReadHTTP(self): 
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        createdFileContent = self.cifsCreateFile(fileName, fileContent)       
        readFileContent = self.httpReadFile( TestConfig.userAname, TestConfig.userApass,fileName) 
        self.assertEqual(createdFileContent,readFileContent) 
        self.cifsUnmount()
        return
    
    def testUserAUpdateCIFSUserAReadCIFS(self): 
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        fileUpdateContent= 'Test update of file\n'
        self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        self.cifsCreateFile(fileName, fileContent)       
        self.cifsUpdateFile(fileName, fileUpdateContent)
        updatedFileContent = fileContent + fileUpdateContent
        readFileContent = self.cifsReadFile(fileName)
        self.assertEqual(updatedFileContent,readFileContent) 
        self.cifsUnmount()
        return
    
    def testUserAUpdateHTTPUserAReadCIFS(self): 
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        fileUpdateContent= 'Test update of file\n'
        self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        self.cifsCreateFile(fileName, fileContent)       
        updatedFileContent= fileContent + fileUpdateContent
        # HTTP Update overwrites(does not append the original) the file, hence expecting the updated content when read again.
        updateMessage = self.httpUpdateFile(TestConfig.userAname, TestConfig.userApass,fileName,updatedFileContent)
        self.assertEqual(updateMessage[0],0,"Update file failed: "+str(updateMessage))
        readFileContent = self.cifsReadFile(fileName) 
        self.assertEqual(updatedFileContent,readFileContent) 
        self.cifsUnmount()
        return
    
    def testUserACreateCIFSUserADeleteCIFS(self): 
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        self.cifsCreateFile(fileName, fileContent)     
        self.cifsDeleteFile(fileName)
        self.cifsUnmount()
        return
    
    def testUserACreateCIFSUserADeleteHTTP(self): 
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        self.cifsCreateFile(fileName, fileContent)
        deleteMessage = self.httpDeleteFile(TestConfig.userAname, TestConfig.userApass, fileName)
        self.assertEqual(deleteMessage[0],0,"Delete file failed: "+str(deleteMessage))
        self.cifsUnmount()
        return

    def testUserACreateHTTPUserAReadHTTP(self): 
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        createMessage = self.httpCreateFile(TestConfig.userAname, TestConfig.userApass, fileName, fileContent) 
        self.assertEqual(createMessage[0],0,"Create file failed: "+str(createMessage))
        readFileContent = self.httpReadFile(TestConfig.userAname, TestConfig.userApass,fileName)        
        self.assertEqual(fileContent,readFileContent) 
        return
  
    def testUserACreateHTTPUserAReadCIFS(self): 
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        createMessage = self.httpCreateFile(TestConfig.userAname, TestConfig.userApass, fileName, fileContent) 
        self.assertEqual(createMessage[0],0,"Create file failed: "+str(createMessage))
        readFileContent = self.cifsReadFile(fileName) 
        self.assertEqual(fileContent,readFileContent) 
        self.cifsUnmount()
        return
       
    def testUserAUpdateHTTPUserAReadHTTP(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        fileUpdateContent= 'Test update of file\n'     
        createMessage = self.httpCreateFile(TestConfig.userAname, TestConfig.userApass, fileName, fileContent)
        self.assertEqual(createMessage[0],0,"Create file failed: "+str(createMessage)) 
        updateMessage = self.httpUpdateFile(TestConfig.userAname, TestConfig.userApass,fileName,fileUpdateContent)
        self.assertEqual(updateMessage[0],0,"Update file failed: "+str(updateMessage))
        readFileContent = self.httpReadFile(TestConfig.userAname, TestConfig.userApass,fileName)
        self.assertEqual(fileUpdateContent,readFileContent) 
        return 
    
    def testUserAUpdateCIFSUserAReadHTTP(self): 
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        fileUpdateContent= 'Test update of file\n'     
        createMessage = self.httpCreateFile(TestConfig.userAname, TestConfig.userApass, fileName, fileContent)
        self.assertEqual(createMessage[0],0,"Create file failed: "+str(createMessage)) 
        self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        self.cifsUpdateFile(fileName, fileUpdateContent)
        updatedFileContent= fileContent + fileUpdateContent
        readFileContent = self.httpReadFile(TestConfig.userAname, TestConfig.userApass,fileName) 
        self.assertEqual(updatedFileContent,readFileContent) 
        self.cifsUnmount()
        return
       
    def testUserACreateHTTPUserADeleteHTTP(self): 
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        fileUpdateContent= 'Test update of file\n'     
        createMessage = self.httpCreateFile(TestConfig.userAname, TestConfig.userApass, fileName, fileContent)
        self.assertEqual(createMessage[0],0,"Create file failed: "+str(createMessage))
        deleteMessage = self.httpDeleteFile(TestConfig.userAname, TestConfig.userApass, fileName)
        self.assertEqual(deleteMessage[0],0,"Delete file failed: "+str(deleteMessage))
        return
        
    def testUserACreateHTTPUserADeleteCIFS(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        fileUpdateContent= 'Test update of file\n'     
        createMessage = self.httpCreateFile(TestConfig.userAname, TestConfig.userApass, fileName, fileContent)
        self.assertEqual(createMessage[0],0,"Create file failed: "+str(createMessage))
        self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        self.cifsDeleteFile(fileName)
        self.cifsUnmount()
        return
    
    
    # Test User B's access permissions on files in User A's collab area
    
    def testUserBCreateCIFSInUserA(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        self.cifsMountAs(TestConfig.userAname, TestConfig.userBname, TestConfig.userBpass)
        allowed = True
        try:
            self.cifsCreateFile(fileName, fileContent)
        except IOError as e:
            self.assertEqual(e.errno, 13, "Operation should fail with error 13, was: "+str(e))
            self.assertEqual(e.strerror, "Permission denied", "Operation should fail with 'Permission denied', was: "+str(e))
            allowed = False
        assert allowed, "User B is not able to create a file in User A's filespace by WebDAV!"
        self.cifsUnmount()
        return
    
    def testUserACreateCIFSUserBReadCIFS(self):      
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        
        self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        self.cifsCreateFile(fileName, fileContent)
        self.cifsUnmount()
        
        self.cifsMountAs(TestConfig.userAname, TestConfig.userBname, TestConfig.userBpass)
        readFileContent = self.cifsReadFile(fileName) 
        self.assertEqual(fileContent,readFileContent) 
        self.cifsUnmount()
        return
    
    def testUserACreateCIFSUserBUpdateCIFS(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        fileUpdateContent= 'Test update of file\n'     
        self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        self.cifsCreateFile(fileName, fileContent)
        self.cifsUnmount()
        self.cifsMountAs(TestConfig.userAname, TestConfig.userBname, TestConfig.userBpass)
        allowed = True
        try:
            self.cifsUpdateFile(fileName,fileUpdateContent)
        except IOError as e:
            self.assertEqual(e.errno, 13, "Operation should fail with error 13, was: "+str(e))
            self.assertEqual(e.strerror, "Permission denied", "Operation should fail with 'Permission denied', was: "+str(e))
            allowed = False
        assert allowed, "User B is not able to update a file in User A's filespace by WebDAV!"
        self.cifsUnmount()
        return

    def testUserACreateCIFSUserBDeleteCIFS(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        fileUpdateContent= 'Test update of file\n'     
        self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        self.cifsCreateFile(fileName, fileContent)
        self.cifsUnmount()
        self.cifsMountAs(TestConfig.userAname, TestConfig.userBname, TestConfig.userBpass)
        deleteMessage = self.cifsDeleteFile(fileName)
        self.assertNotEquals(deleteMessage[0], 13, 
                          "Not Expected (13, Permission denied) for "+TestConfig.cifsmountpoint + '/'+ fileName+"'"+
                          ", got: "+str(deleteMessage))
        self.cifsUnmount()
        return
    
    def testUserBCreateHTTPInUserA(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        createMessage = self.httpCreateFileAs(TestConfig.userAname, TestConfig.userBname, TestConfig.userBpass, fileName, fileContent)
        #self.assertEqual(createMessage[0], 401, "User B can create a file in User A's filespace by HTTP, got: "+str(createMessage))
        self.assertEqual(createMessage[0],0,"Create file failed: "+str(createMessage))
        return
    
    def testUserACreateHTTPUserBReadHTTP(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'  
        createMessage = self.httpCreateFile(TestConfig.userAname, TestConfig.userApass, fileName, fileContent)
        self.assertEqual(createMessage[0],0,"Create file failed: "+str(createMessage))
        readFileContent = self.httpReadFileAs(TestConfig.userAname, TestConfig.userBname, TestConfig.userBpass, fileName)
        self.assertEqual(fileContent,readFileContent,"User B cannot read the file in User A's filespace by HTTP")
        return      
    
    def testUserACreateHTTPUserBUpdateHTTP(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'  
        fileUpdateContent= 'Test update of file\n'     
        createMessage = self.httpCreateFile(TestConfig.userAname, TestConfig.userApass, fileName, fileContent)
        self.assertEqual(createMessage[0],0,"Create file failed: "+str(createMessage))
        updateMessage = self.httpUpdateFileAs(TestConfig.userAname, TestConfig.userBname, TestConfig.userBpass, fileName,fileUpdateContent)        
        self.assertNotEquals(updateMessage[0], 401, 
                          "Not Expected (401, basic authentication failed) for "+TestConfig.cifsmountpoint + '/'+ fileName+"'"+
                          ", got: "+str(updateMessage))
        return
        
    def testUserACreateHTTPUserBDeleteHTTP(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'  
        createMessage = self.httpCreateFile(TestConfig.userAname, TestConfig.userApass, fileName, fileContent)
        self.assertEqual(createMessage[0],0,"Create file failed: "+str(createMessage))
        deleteMessage = self.httpDeleteFileAs(TestConfig.userAname, TestConfig.userBname, TestConfig.userBpass, fileName)
        #print repr(deleteMessage)
        self.assertNotEquals(deleteMessage[0], 401, 
                          "Not Expected (401, basic authentication failed) for "+TestConfig.cifsmountpoint + '/'+ fileName+"'"+
                          ", got: "+str(deleteMessage))
        return
  
    # Sentinel/placeholder tests

   # Test Collaborator's access permissions on files in User A's Collab area    
      
    def testCollabCreateCIFSInUserA(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        status = self.cifsMountAs(TestConfig.userAname, TestConfig.collabname, TestConfig.collabpass)
        disallowed = False
        if status!=8192 :
               try:
                    self.cifsCreateFile(fileName, fileContent)
               except IOError as e:
                    self.assertEqual(e.errno, 13, "Operation should fail with error 13, was: "+str(e))
                    self.assertEqual(e.strerror, "Permission denied", "Operation should fail with 'Permission denied', was: "+str(e))
                    disallowed = True
               assert disallowed, "Collaborator can create a file in User A's filespace by WebDAV!"
               self.cifsUnmount()
        return
     
    def testUserACreateCIFSCollabReadCIFS(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        self.cifsCreateFile(fileName, fileContent)
        self.cifsUnmount()
        status = self.cifsMountAs(TestConfig.userAname, TestConfig.collabname, TestConfig.collabpass)
        allowed = True
        if status!=8192 :
            try:
                self.cifsReadFile(fileName)
            except IOError as e:
                self.assertEqual(e.errno, 13, "Operation should fail with error 13, was: "+str(e))
                self.assertEqual(e.strerror, "Permission denied", "Operation should fail with 'Permission denied', was: "+str(e))
                allowed = False
            assert allowed, "Collaborator is not able to read a file in User A's filespace by WebDAV!"        
            self.cifsUnmount()
        return
    
    def testUserACreateCIFSCollabUpdateCIFS(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        fileUpdateContent= 'Test update of file\n'     
        status  = self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        self.cifsCreateFile(fileName, fileContent)
        self.cifsUnmount()
        status = self.cifsMountAs(TestConfig.userAname, TestConfig.collabname, TestConfig.collabpass)
        if status!=8192 :
            disallowed = False
            try:
                self.cifsUpdateFile(fileName,fileUpdateContent)
            except IOError as e:
                self.assertEqual(e.errno, 13, "Operation should fail with error 13, was: "+str(e))
                self.assertEqual(e.strerror, "Permission denied", "Operation should fail with 'Permission denied', was: "+str(e))
                disallowed = True
                assert disallowed, "Collaborator can update a file in User A's filespace by WebDAV!"
                self.cifsUnmount()
        return

    def testUserACreateCIFSCollabDeleteCIFS(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        fileUpdateContent= 'Test update of file\n'     
        self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        self.cifsCreateFile(fileName, fileContent)
        self.cifsUnmount()
        status = self.cifsMountAs(TestConfig.userAname, TestConfig.collabname, TestConfig.collabpass)
        if status!=8192 :
            deleteMessage = self.cifsDeleteFile(fileName)
            self.assertEquals(deleteMessage[0], 13, 
                          "Expected (13, Permission denied) for "+TestConfig.cifsmountpoint + '/'+ fileName+"'"+
                          ", got: "+str(deleteMessage))
            self.cifsUnmount()
        return
    
    def testCollabCreateHTTPInUserA(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        createMessage = self.httpCreateFileAs(TestConfig.userAname, TestConfig.collabname, TestConfig.collabpass, fileName, fileContent)
        self.assertEqual(createMessage[0], 401, "User B is able to create a file in User A's filespace by HTTP, got: "+str(createMessage))
        return
    
    def testUserACreateHTTPCollabReadHTTP(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'  
        createMessage = self.httpCreateFile(TestConfig.userAname, TestConfig.userApass, fileName, fileContent)
        self.assertEqual(createMessage[0],0,"Create file failed: "+str(createMessage))
        allowed = True
        try:
            self.httpReadFileAs(TestConfig.userAname, TestConfig.collabname, TestConfig.collabpass, fileName)
        except urllib2.HTTPError as e:
            self.assertEqual(e.code, 401, "Operation should be 401 (auth failed), was: "+str(e))
            allowed = False
        assert allowed, "Collaborator is not able to read a file in User A's filespace by HTTP!"
        return      
    
    def testUserACreateHTTPCollabUpdateHTTP(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'  
        createMessage = self.httpCreateFile(TestConfig.userAname, TestConfig.userApass, fileName, fileContent)
        self.assertEqual(createMessage[0],0,"Create file failed: "+str(createMessage))
        updateMessage = self.httpUpdateFileAs(TestConfig.userAname, TestConfig.collabname, TestConfig.collabpass, fileName,fileContent)
        self.assertEquals(updateMessage[0], 401, 
                          "Expected (401, basic authentication failed) for "+TestConfig.cifsmountpoint + '/'+ fileName+"'"+
                          ", got: "+str(updateMessage))
        return
        
    
    def testUserACreateHTTPCollabDeleteHTTP(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'  
        createMessage = self.httpCreateFile(TestConfig.userAname, TestConfig.userApass, fileName, fileContent)
        self.assertEqual(createMessage[0],0,"Create file failed: "+str(createMessage))
        deleteMessage = self.httpDeleteFileAs(TestConfig.userAname, TestConfig.collabname, TestConfig.collabpass, fileName)
        self.assertEquals(deleteMessage[0], 401, 
                          "Expected (401, basic authentication failed) for "+TestConfig.cifsmountpoint + '/'+ fileName+"'"+
                          ", got: "+str(deleteMessage))
        return
    
    
     # Test RG Leader's access permissions on files in User A's Collab area
    
    def testRGLeaderCreateCIFSInUserA(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        createMessage = self.httpCreateFileAs(TestConfig.userAname, TestConfig.userRGleadername, TestConfig.userRGleaderpass, fileName, fileContent)
        self.assertNotEqual(createMessage[0], 401, "RG Leader can create a file in User A's filespace by HTTP, got: "+str(createMessage))  
        return
      
    def testUserACreateCIFSRGLeaderReadCIFS(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        self.cifsCreateFile(fileName, fileContent)
        self.cifsUnmount()
        self.cifsMountAs(TestConfig.userAname, TestConfig.userRGleadername, TestConfig.userRGleaderpass)
        allowed = True       
        try: 
            self.cifsReadFile(fileName)
        except IOError as e:
            self.assertEqual(e.errno, 13, "Operation should fail with error 13, was: "+str(e))
            self.assertEqual(e.strerror, "Permission denied", "Operation should fail with 'Permission denied', was: "+str(e))
            allowed = False
        assert allowed, "Research Group Leader is not able to read a file in User A's filespace by WebDAV!"        
        self.cifsUnmount()
        return
     
    def testUserACreateCIFSRGLeaderUpdateCIFS(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        fileUpdateContent= 'Test update of file\n'     
        self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        self.cifsCreateFile(fileName, fileContent)
        self.cifsUnmount()
        self.cifsMountAs(TestConfig.userAname, TestConfig.userRGleadername, TestConfig.userRGleaderpass)
        allowed = True
        try:
            self.cifsUpdateFile(fileName,fileUpdateContent)
        except IOError as e:
            self.assertEqual(e.errno, 13, "Operation should fail with error 13, was: "+str(e))
            self.assertEqual(e.strerror, "Permission denied", "Operation should fail with 'Permission denied', was: "+str(e))
            allowed = True
        assert allowed, "Research Group Leader is not able to update a file in User A's filespace by WebDAV!"
        self.cifsUnmount()
        return
     
    def testUserACreateCIFSRGLeaderDeleteCIFS(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        fileUpdateContent= 'Test update of file\n'     
        self.cifsMount(TestConfig.userAname, TestConfig.userApass)
        self.cifsCreateFile(fileName, fileContent)
        self.cifsUnmount()
        self.cifsMountAs(TestConfig.userAname, TestConfig.userRGleadername, TestConfig.userRGleaderpass)
        deleteMessage = self.cifsDeleteFile(fileName)
        self.assertNotEquals(deleteMessage[0], 13, 
                          "Not Expected (13, Permission denied) for "+TestConfig.cifsmountpoint + '/'+ fileName+"'"+
                          ", got: "+str(deleteMessage))
        self.cifsUnmount()
        return
     
    def testRGLeaderCreateHTTPInUserA(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'
        createMessage = self.httpCreateFileAs(TestConfig.userAname, TestConfig.userRGleadername, TestConfig.userRGleaderpass, fileName, fileContent)
        self.assertNotEqual(createMessage[0], 401, "Research Group Leader is not able to create a file in User A's filespace by HTTP, got: "+str(createMessage))
        return
     
    def testUserACreateHTTPRGLeaderReadHTTP(self):   
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'  
        createMessage = self.httpCreateFile(TestConfig.userAname, TestConfig.userApass, fileName, fileContent)
        self.assertEqual(createMessage[0],0,"Create file failed: "+str(createMessage))
        readFileContent = self.httpReadFileAs(TestConfig.userAname, TestConfig.userRGleadername, TestConfig.userRGleaderpass, fileName)
        self.assertEqual(fileContent,readFileContent,"Research Group Leader is not able to read the file in User A's filespace by HTTP")
        return
     
    def testUserACreateHTTPRGLeaderUpdateHTTP(self): 
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'  
        createMessage = self.httpCreateFile(TestConfig.userAname, TestConfig.userApass, fileName, fileContent)
        self.assertEqual(createMessage[0],0,"Create file failed: "+str(createMessage))
        updateMessage = self.httpUpdateFileAs(TestConfig.userAname, TestConfig.userRGleadername, TestConfig.userRGleaderpass, fileName,fileContent)
        self.assertNotEquals(updateMessage[0], 401, 
                          "Not Expected (401, basic authentication failed) for "+TestConfig.cifsmountpoint + '/'+ fileName+"'"+
                          ", got: "+str(updateMessage))
        return
     
    def testUserACreateHTTPRGLeaderDeleteHTTP(self):
        fileName = 'testCreateFileCIFS.tmp'
        fileContent= 'Test creation of file\n'  
        createMessage = self.httpCreateFile(TestConfig.userAname, TestConfig.userApass, fileName, fileContent)
        self.assertEqual(createMessage[0],0,"Create file failed: "+str(createMessage))
        deleteMessage = self.httpDeleteFileAs(TestConfig.userAname, TestConfig.userRGleadername, TestConfig.userRGleaderpass, fileName)
        self.assertNotEquals(deleteMessage[0], 401, 
                          "Not Expected (401, basic authentication failed) for "+TestConfig.cifsmountpoint + '/'+ fileName+"'"+
                          ", got: "+str(deleteMessage))
        return
    

    def testUnits(self):
        assert (True)

    def testComponents(self):
        assert (True)

    def testIntegration(self):
        assert (True)

    def testPending(self):
        assert (False), "No pending test"

# Assemble test suite

from MiscLib import TestUtils

def getTestSuite(select="unit"):
    """
    Get test suite

    select  is one of the following:
            "unit"      return suite of unit tests only
            "component" return suite of unit and component tests
            "all"       return suite of unit, component and integration tests
            "pending"   return suite of pending tests
            name        a single named test to be run
    """
    testdict = {
        "unit": 
            [ "testUnits"
            , "testNull"
            # Test User A's access permissions in his own Collab area
            , "testUserACreateCIFSUserAReadCIFS"
            , "testUserACreateCIFSUserAReadHTTP"
            , "testUserAUpdateCIFSUserAReadCIFS"
            , "testUserAUpdateHTTPUserAReadCIFS"
            , "testUserACreateCIFSUserADeleteCIFS"
            , "testUserACreateCIFSUserADeleteHTTP"
            , "testUserACreateHTTPUserAReadHTTP"           
            , "testUserACreateHTTPUserAReadCIFS"
            , "testUserAUpdateHTTPUserAReadHTTP"
            , "testUserAUpdateCIFSUserAReadHTTP"
            , "testUserACreateHTTPUserADeleteHTTP"
            , "testUserACreateHTTPUserADeleteCIFS"
            # Test User B's access permissions on files in User A's Collab area
            , "testUserBCreateCIFSInUserA"
            , "testUserACreateCIFSUserBReadCIFS"
            , "testUserACreateCIFSUserBUpdateCIFS"
            , "testUserACreateCIFSUserBDeleteCIFS"
            , "testUserBCreateHTTPInUserA"
            , "testUserACreateHTTPUserBReadHTTP"
            , "testUserACreateHTTPUserBUpdateHTTP"
            , "testUserACreateHTTPUserBDeleteHTTP"  
            # Test Collaborator's access permissions on files in User A's Collab area         
            , "testCollabCreateCIFSInUserA"
            , "testUserACreateCIFSCollabReadCIFS"
            , "testUserACreateCIFSCollabUpdateCIFS"
            , "testUserACreateCIFSCollabDeleteCIFS"
            , "testCollabCreateHTTPInUserA"
            , "testUserACreateHTTPCollabReadHTTP"
            , "testUserACreateHTTPCollabUpdateHTTP"
            , "testUserACreateHTTPCollabDeleteHTTP"       
            # Test RG Leader's access permissions on files in User A's Collab area     
            , "testRGLeaderCreateCIFSInUserA"
            , "testUserACreateCIFSRGLeaderReadCIFS"
            , "testUserACreateCIFSRGLeaderUpdateCIFS"
            , "testUserACreateCIFSRGLeaderDeleteCIFS"
            , "testRGLeaderCreateHTTPInUserA"
            , "testUserACreateHTTPRGLeaderReadHTTP"
            , "testUserACreateHTTPRGLeaderUpdateHTTP"
            , "testUserACreateHTTPRGLeaderDeleteHTTP"
            ],
        "component":
            [ "testComponents"
            ],
        "integration":
            [ "testIntegration"
            ],
        "pending":
            [ "testPending"
            ]
        }
    return TestUtils.getTestSuite(TestFileCollabArea, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestFileCollabArea.log", getTestSuite, sys.argv)

# End.



   
