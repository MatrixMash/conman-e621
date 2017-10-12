package conman;

import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class ConMan {
	
	public static final URL E621_URL;
	public static final String USER_AGENT = "ConMan/1.1 (e621 tagging interface by MatrixMash)";
	//"b164db86d860c6178bec6ff97d07dd52";	//Referred to (legacy reasons) as "password_hash".
	//public static final String LOGIN_TOKEN = "login=" + "MatrixMash" + "&password_hash=" + "b164db86d860c6178bec6ff97d07dd52";
	//webLink.setRequestProperty("login", LOGIN);
	//webLink.setRequestProperty("password_hash", API_KEY);
	
	static {
		String e621 = "https://www.e621.net/";
		try {
			E621_URL = new URL(e621);
		} catch(MalformedURLException e) {
			throw new RuntimeException("URL " + e621 + " is apparently not valid. This should not be possible.", e);
		}
	}
	
	public static void main(String[] args) throws Exception {
		System.out.println("Still alive");
	}
}

		/*
		URLConnection webLink = E621_URL.openConnection();
		webLink.setRequestProperty("User-Agent", USER_AGENT);
		BufferedReader stuff = new BufferedReader(
			new InputStreamReader(webLink.getInputStream())
		);
		String inputLine;
		while((inputLine = stuff.readLine()) != null)
			System.out.println(inputLine);
		stuff.close();*/