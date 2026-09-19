import java.io.PrintWriter;
import java.io.BufferedReader;
import java.io.OutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

class Server {
    private static ServerSocket serverSocket;
    private static Socket clientSocket;
    private static BufferedReader in;
    private static PrintWriter out;
    private static String output = "";
    private static String eor = "[EOR]"; // a code for end-of-response
    private static int count = 0;
    private static final String expectedUsername = System.getenv("SCHOOL_SERVER_USERNAME");
    private static final String expectedPassword = System.getenv("SCHOOL_SERVER_PASSWORD");
    
    // establishing a connection
    private static void setup() throws IOException {
        
        serverSocket = new ServerSocket(0);
        toConsole("Server port is " + serverSocket.getLocalPort());
        
        clientSocket = serverSocket.accept();

        // get the input stream and attach to a buffered reader
        in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
        
        // get the output stream and attach to a printwriter
        out = new PrintWriter(clientSocket.getOutputStream(), true);

        toConsole("Accepted connection from "
                 + clientSocket.getInetAddress() + " at port "
                 + clientSocket.getPort());
            
        sendGreeting();
        
    }
    
    // the initial message sent from server to client
    private static void sendGreeting()
    {
        appendOutput("Welcome to Catnet!\n");
    }
    
    
    
    // what happens while client and server are connected
    private static void talk() throws IOException {
        /* placing echo functionality into a separate private method allows it to be easily swapped for a different behaviour */
    	
	    	if (expectedUsername == null || expectedPassword == null) {
	    		throw new IllegalStateException("Set SCHOOL_SERVER_USERNAME and SCHOOL_SERVER_PASSWORD before starting the server.");
	    	}
	    	userCredential();
    	passCredential();
    	echoClient();
        disconnect();
    }
    
    // repeatedly take input from client and send back in upper case
    private static void echoClient() throws IOException
    {
    	String echoLine;
	    	appendOutput("Welcome!\n");
    	appendOutput("Type a message and i will echo it");
    	sendOutput();
    	while((echoLine = in.readLine())!= null) {
    	appendOutput(echoLine.toUpperCase());
    	sendOutput();
        toConsole(echoLine);
    	}
    }
    
    private static void userCredential() throws IOException
    {
    	
    	String usernameLine;
    	appendOutput("\nEnter username: ");
    	sendOutput();
    	toConsole("Username requested");
    	
        while (!(usernameLine = in.readLine()).equals(expectedUsername)) {
            
        	appendOutput("Username not recognized\n");
        	appendOutput("Enter username: ");
        	sendOutput();
        	toConsole("Username not recognized");
        	toConsole("Username requested");
            
        
        	
        }
        
        toConsole("Username accepted");
        return;
        
    }
    
    private static void passCredential() throws IOException{
    	appendOutput("Enter password:");
    	sendOutput();
    	toConsole("Password requested");
    	String passwordLine;
    	
	    	while(!(passwordLine = in.readLine()).equals(expectedPassword)) {
    		count +=1;
    		if(count == 3) {
    			appendOutput("Third failed password attempt. You're now disconnected");
    			sendOutput();
    			disconnect();
    			
    		}
    		appendOutput("Password not recognized\n");
	    		toConsole("Password not recognized");
    		userCredential();
    		appendOutput("Enter password: ");
    		sendOutput();
    		toConsole("Password requested");
    		
    	}
	    	toConsole("Username and password verified");
    	return;
    }
    
    private static void disconnect() throws IOException {
        out.close();
        toConsole("Disconnected.");
        System.exit(0);
    }
    
    // add a line to the next message to be sent to the client
    private static void appendOutput(String line) {
        output += line + "\r";
    }
    
    // send next message to client
    private static void sendOutput() {
        out.println( output + "[EOR]");
        out.flush();
        output = "";
    }
    
    // because it makes life easier!
    private static void toConsole(String message) {
        System.out.println(message);
    }
    
    public static void main(String[] args) {
        try {
            setup();
            talk();
        }
        catch( IOException ioex ) {
            toConsole("Error: " + ioex );
        }
    }
}
