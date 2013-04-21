package spokenc.logs;

public class LogEntry {
	protected String fileName;
	protected int fileLine;
	
	public LogEntry(String fileName, int fileLine) {
		this.fileName = fileName;
		this.fileLine = fileLine;
	}
	
	public String getFileName() {
		return fileName;
	}

	public void setFileName(String fileName) {
		this.fileName = fileName;
	}

	public int getFileLine() {
		return fileLine;
	}

	public void setFileLine(int fileLine) {
		this.fileLine = fileLine;
	}
	
	public String getLocation() {
		return fileName + ":" + fileLine;
	}

	public String toString() {
		return fileName + ":" + fileLine;
	}
	
	public static String getDescriptor() {
		return "logEntry";
	}
	
}
