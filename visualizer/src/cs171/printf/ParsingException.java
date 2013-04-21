package cs171.printf;

public class ParsingException extends Exception {
	private static final long serialVersionUID = -5846243129418222990L;
	
	private String line;
	public ParsingException(String line) {
		this.line = line;
	}
	
	public String getLine() {
		return line;
	}
}
