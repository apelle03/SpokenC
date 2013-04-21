package cs171.printf;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import cs171.printf.logs.FuncCall;
import cs171.printf.logs.FuncReturn;
import cs171.printf.logs.Log;
import cs171.printf.logs.LogEntry;
import cs171.printf.logs.ScopeIn;
import cs171.printf.logs.ScopeOut;
import cs171.printf.logs.VarAssignment;
import cs171.printf.logs.VarDeclaration;
import cs171.printf.logs.types.VarType;
import cs171.printf.logs.types.VarValue;

public class LogParser {
	public static Log ParseLog(File logFile) {		
		try {
			BufferedReader in = new BufferedReader(new FileReader(logFile));
			Log log = new Log();
			
			String line;
			while ((line = in.readLine()) != null) {
				try {
					log.addLogItem(ParseLine(line));
				} catch (ParsingException e) {
					System.out.println("Error parsing line: " + e.getLine());
					e.printStackTrace();
					in.close();
					return null;
				}
			}
			in.close();
			return log;
		} catch (FileNotFoundException e) {
			System.out.println("Error opening file: " + logFile);
			e.printStackTrace();
		} catch (IOException e) {
			System.out.println("Error reading file: " + logFile);
			e.printStackTrace();
		}
		return null;
	}
	
	public static LogEntry ParseLine(String text) throws ParsingException {
		String parts[] = text.split(":", 3);
		if (parts.length != 3) {
			throw new ParsingException(text);
		}
		LogEntry entry = null;
		String name = parts[0];
		int line = Integer.parseInt(parts[1]);
		if (parts[2].startsWith("call")) {
			String arg = parts[2].substring(parts[2].indexOf('(') + 1, parts[2].length() - 1);
			entry = new FuncCall(name, line, arg);
		} else if (parts[2].startsWith("return")) {
			String arg = parts[2].substring(parts[2].indexOf('(') + 1, parts[2].length() - 1);
			String args[] = arg.split(",", 2);
			entry = new FuncReturn(name, line, args[0], ParseValue(args[1]));
		} else if (parts[2].startsWith("scope_in")) {
			entry = new ScopeIn(name, line);
		} else if (parts[2].startsWith("scope_out")) {
			entry = new ScopeOut(name, line);
		} else if (parts[2].startsWith("decl")) {
			String arg = parts[2].substring(parts[2].indexOf('(') + 1, parts[2].length() - 1);
			entry = new VarDeclaration(name, line, ParseValue(arg));
		} else if (parts[2].startsWith("assign")) {
			String arg = parts[2].substring(parts[2].indexOf('(') + 1, parts[2].length() - 1);
			entry = new VarAssignment(name, line, ParseValue(arg));
		} else {
			throw new ParsingException(text);
		}
		return entry;
	}
	
	public static VarValue ParseValue(String text) throws ParsingException {
		String[] varParts = text.split(",");
		VarType type = VarType.fromString(varParts[0]);
		if (type == null) {
			throw new ParsingException(text);
		}
		if (varParts.length == 2) {
			return new VarValue(type, varParts[1]);
		} else if (varParts.length == 3) {
			return new VarValue(type, varParts[1], varParts[2]);
		} else {
			throw new ParsingException(text);
		}
	}
}
