package cs171.printf;

import java.awt.Color;
import java.lang.reflect.InvocationTargetException;

import cs171.printf.logs.LogEntry;

public class LogFilter {
	private Class<? extends LogEntry> type;
	private Color color;
	private String descriptor;
	
	public LogFilter(Class<? extends LogEntry> type, Color color) {
		this.type = type;
		this.color = color;
		try {
			this.descriptor = (String)type.getDeclaredMethod("getDescriptor", (Class<?>[])null).invoke(null, (Object[])null);
		} catch (IllegalAccessException | IllegalArgumentException
				| InvocationTargetException | NoSuchMethodException
				| SecurityException e) {
			e.printStackTrace();
		}
	}

	public Class<? extends LogEntry> getType() {
		return type;
	}

	public void setType(Class<? extends LogEntry> type) {
		this.type = type;
	}

	public Color getColor() {
		return color;
	}

	public void setColor(Color color) {
		this.color = color;
	}

	public String getDescriptor() {
		return descriptor;
	}
	
	public boolean equals(Object obj) {
		if (obj instanceof LogEntry) {
			return type.equals(((LogFilter)obj).type);
		} else {
			return false;
		}
	}
}
