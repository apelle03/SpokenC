package cs171.printf;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import javax.swing.JCheckBox;
import javax.swing.JTextPane;
import javax.swing.text.BadLocationException;
import javax.swing.text.DefaultStyledDocument;
import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;
import javax.swing.text.StyledDocument;

import cs171.printf.logs.Log;
import cs171.printf.logs.LogEntry;

public class LogDisplayManager {
	private Log log;
	
	private Set<LogFilter> filters;
	private StyledDocument styledLog;
	
	private JTextPane logTextArea;
	
	private JCheckBox all;
	private Map<JCheckBox, LogFilter> filterSelectors;
	
	public LogDisplayManager() {
		filters = new HashSet<>();
		filterSelectors = new HashMap<>();
	}
	
	public void setLogView(JTextPane logTextArea) {
		this.logTextArea = logTextArea;
	}
	
	public void setAllSelector(JCheckBox all) {
		this.all = all;
		this.all.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				selectAll();
			}
		});
	}
	
	public void setFilterSelector(JCheckBox selector, Class<? extends LogEntry> type, Color color) {
		filterSelectors.put(selector, new LogFilter(type, color));
		selector.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if (e.getSource() instanceof JCheckBox) {
					JCheckBox source = (JCheckBox)e.getSource();
					changeFilters(filterSelectors.get(source), source.isSelected());
				}
			}
		});
	}
	
	public void setLog(Log log) {
		this.log = log;
		selectAll();
	}
	
	private void selectAll() {
		filters.addAll(filterSelectors.values());
		updateStyledLog();
		
		all.setSelected(true);
		for (JCheckBox selector : filterSelectors.keySet()) {
			selector.setSelected(false);
		}
	}
	
	private void changeFilters(LogFilter filter, boolean selected) {
		if (selected) {
			if (all.isSelected()) {
				all.setSelected(false);
				filters.clear();
			}
			filters.add(filter);
		} else {
			filters.remove(filter);
			if (filters.isEmpty()) {
				selectAll();
			}
		}
		updateStyledLog();
	}		
		
	public StyledDocument getStyledLog() {
		return styledLog;
	}
	
	private void updateStyledLog() {
		styledLog = new DefaultStyledDocument();
		String text = log.toString(filters);
		
		try {
			styledLog.insertString(0, text, null);
		} catch (BadLocationException e) {
			e.printStackTrace();
		}
		
		SimpleAttributeSet highlight = new SimpleAttributeSet();
		for (LogFilter filter : filters) {
			StyleConstants.setBackground(highlight, filter.getColor());
			int offset = text.indexOf(filter.getDescriptor());
			int length = -1;
			while (offset != -1) {
				length = filter.getDescriptor().length();
				styledLog.setCharacterAttributes(offset, length, highlight, false);
				offset = text.indexOf(filter.getDescriptor(), offset + length);
			}
		}
		logTextArea.setDocument(styledLog);
	}
}
