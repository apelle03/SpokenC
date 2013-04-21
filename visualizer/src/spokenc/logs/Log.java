package spokenc.logs;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import spokenc.LogFilter;


public class Log {
	private List<LogEntry> logItems;
	
	public Log() {
		logItems = new ArrayList<>();
	}

	public List<? extends LogEntry> getLogItems() {
		return logItems;
	}

	public void setLogItems(List<LogEntry> logItems) {
		this.logItems = logItems;
	}
	
	public void addLogItem(LogEntry item) {
		logItems.add(item);
	}
	
	public String toString() {
		String s = "";
		for (LogEntry item : logItems) {
			s += item.toString() + "\n";
		}
		return s;
	}
	
	public String toString(Set<LogFilter> types) {
		String s = "";
		for (LogEntry item : logItems) {
			for (LogFilter type : types) {
				if (type.getType() == item.getClass()) {
					s += item.toString() +"\n";
				}
			}
		}
		return s;
	}
}
