package cs171.printf;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Paint;
import java.awt.Shape;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ComponentEvent;
import java.awt.event.ComponentListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.awt.event.KeyEvent;
import java.awt.geom.Rectangle2D;
import java.awt.geom.RoundRectangle2D;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;
import java.util.Stack;

import javax.swing.GroupLayout;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSeparator;
import javax.swing.JSplitPane;
import javax.swing.JTabbedPane;
import javax.swing.JTextArea;
import javax.swing.JTextPane;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.text.DefaultStyledDocument;
import javax.swing.text.StyledDocument;

import org.apache.commons.collections15.Transformer;

import cs171.printf.environment.Edge;
import cs171.printf.environment.FunctionScope;
import cs171.printf.environment.Variable;
import cs171.printf.logs.FuncCall;
import cs171.printf.logs.FuncReturn;
import cs171.printf.logs.Log;
import cs171.printf.logs.LogEntry;
import cs171.printf.logs.ScopeIn;
import cs171.printf.logs.ScopeOut;
import cs171.printf.logs.VarAssignment;
import cs171.printf.logs.VarDeclaration;
import edu.uci.ics.jung.algorithms.layout.Layout;
import edu.uci.ics.jung.graph.DirectedSparseGraph;
import edu.uci.ics.jung.graph.Graph;
import edu.uci.ics.jung.graph.SparseMultigraph;
import edu.uci.ics.jung.graph.util.Context;
import edu.uci.ics.jung.visualization.VisualizationViewer;
import edu.uci.ics.jung.visualization.control.DefaultModalGraphMouse;
import edu.uci.ics.jung.visualization.control.ModalGraphMouse;
import edu.uci.ics.jung.visualization.decorators.EdgeShape;
import edu.uci.ics.jung.visualization.decorators.ToStringLabeller;
import edu.uci.ics.jung.visualization.picking.PickedInfo;
import edu.uci.ics.jung.visualization.renderers.Renderer.VertexLabel.Position;

public class Visualizer extends JFrame {
	private static final long serialVersionUID = -8292202045318205925L;
	
	private static Color getColorFromFunction(String function) {
		Random gen = new Random(function.hashCode());
    	int range = 110;
    	int base = 256 - range;
    	Color c = new Color(gen.nextInt(range) + base, gen.nextInt(range) + base, gen.nextInt(range) + base);
    	return c;
	}
	
	private Log log;
	private LogDisplayManager logDisplayManager;
	
	// Graph
	private Graph<Variable, Edge> graph;
	private Layout<Variable, Edge> layout;
	private VisualizationViewer<Variable, Edge> vv;
	private DefaultModalGraphMouse<Variable, Edge> gm;
	
	// Stack
	private JTextPane stackFrame;
	private JPanel stackPanel;
	private JScrollPane stackFramePane;
	
	// Graph View
	private JSplitPane graphView;
	
	// Log
	private JTextPane logText;
	private JScrollPane logScroll;
	private JCheckBox logAll, logCall, logReturn, logIn, logOut, logDecl, logAssign;
	private JPanel logView;
	
	// Source
	private JTabbedPane sourceTabs;
	private JButton setSource;
	private JPanel sourceView;
	
	// Log View
	private JSplitPane textView;
	
	// View Container
	private JTabbedPane viewPane;
	
	// Menus
	private JMenuBar menuBar;
	private JMenu mnuFile;
	private JMenuItem itemOpenLog, itemExit;
	private JMenu mnuView;
	private JMenuItem itemTransformMode, itemPickingMode;
	private JMenu mnuHelp;
	private JMenuItem itemAbout;
	
	// Dialog Boxes
	private JFileChooser logChooser, sourceChooser;
		
	public Visualizer() {		
		// SETUP GRAPH VIEW AREA
		initGraphView();
		
		// SETUP TEXT VIEW AREA
		initTextView();
		
		// SETUP MENUS
		initMenus();
		
		// SETUP THIS FRAME
		viewPane = new JTabbedPane(JTabbedPane.TOP, JTabbedPane.SCROLL_TAB_LAYOUT);
		viewPane.add("Graph", graphView);
		viewPane.add("Log", textView);
		
		this.addComponentListener(new ComponentListener() {
			public void componentResized(ComponentEvent e) {
				graphView.setDividerLocation(.75);
				textView.setDividerLocation(.5);
			}
			public void componentMoved(ComponentEvent e) {}
			public void componentShown(ComponentEvent e) {}
			public void componentHidden(ComponentEvent e) {}
		});
		this.setDefaultCloseOperation(EXIT_ON_CLOSE);
		this.getContentPane().add(viewPane);
		this.setJMenuBar(menuBar);
		this.setTitle("SpokenC");
		this.pack();
		this.setLocation(50, 50);
		this.setResizable(true);
		
		graphView.setDividerLocation(.75);
		textView.setDividerLocation(.5);
		
		this.setVisible(true);
	}
	
	public void initGraphView() {
		layout = new PrintfLayout(new SparseMultigraph<Variable, Edge>());
		
		gm = new DefaultModalGraphMouse<Variable, Edge>();
		gm.setMode(ModalGraphMouse.Mode.PICKING);
		
		vv = new VisualizationViewer<Variable, Edge>(layout);
		vv.setBackground(Color.WHITE);
		vv.setGraphMouse(gm);
		vv.addKeyListener(gm.getModeKeyListener());
		
		vv.getPickedVertexState().addItemListener(new ItemListener() {
			public void itemStateChanged(ItemEvent e) {
				if (vv.getPickedVertexState().isPicked((Variable)e.getItem())) {
					stackFrame.setDocument(((Variable)e.getItem()).getCallStack());
				} else {
					stackFrame.setDocument(new DefaultStyledDocument());
				}
			}
		});
		
		vv.addComponentListener(new ComponentListener() {
			public void componentResized(ComponentEvent e) {
				layout.setSize(e.getComponent().getSize());
			}
			public void componentMoved(ComponentEvent e) {}
			public void componentShown(ComponentEvent e) {}
			public void componentHidden(ComponentEvent e) {}
		});
		
		stackFrame = new JTextPane();
		stackFrame.setEditable(false);
		stackFrame.setFont(new Font("courier new", Font.PLAIN, 14));
		stackPanel = new JPanel(new BorderLayout());
		stackPanel.add(stackFrame, BorderLayout.CENTER);
		stackFramePane = new JScrollPane(stackPanel);
		graphView = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, vv, stackFramePane);
		graphView.setOneTouchExpandable(true);
		
		//
		// VERTEX
		//
		vv.getRenderContext().setVertexLabelTransformer(new ToStringLabeller<Variable>());
		vv.getRenderContext().setVertexShapeTransformer(new Transformer<Variable, Shape>() {
			public Shape transform(Variable variable) {
				Font font = vv.getRenderContext().getVertexFontTransformer().transform(variable);
				FontMetrics metrics = vv.getFontMetrics(font);
				Rectangle2D bounds = metrics.getStringBounds(vv.getRenderContext().getVertexLabelTransformer().transform(variable), vv.getGraphics());
				return new RoundRectangle2D.Double(
						bounds.getMinX() - bounds.getWidth() / 2 - 4,
						bounds.getMinY() - 2,
						bounds.getWidth() + 8, bounds.getHeight() + 4,
						8, 8);
			}
		});
		final class VertexPaintTransformer implements Transformer<Variable,Paint> {
	        private final PickedInfo<Variable> pi;
	        VertexPaintTransformer(PickedInfo<Variable> pi) { 
	            super();
	            if (pi == null)
	                throw new IllegalArgumentException("PickedInfo instance must be non-null");
	            this.pi = pi;
	        }
	        public Paint transform(Variable v) {
	        	Color c = getColorFromFunction(v.getFunction());
	            if (pi.isPicked(v)){
	                c = c.darker();
	            }
	            return c;
	        }
	    }
		vv.getRenderContext().setVertexFillPaintTransformer(new VertexPaintTransformer(vv.getPickedVertexState()));
		
		
		//
		// EDGE
		//
		vv.getRenderContext().setEdgeLabelTransformer(new ToStringLabeller<Edge>());
		vv.getRenderContext().getEdgeLabelRenderer().setRotateEdgeLabels(false);
		vv.getRenderContext().setEdgeLabelClosenessTransformer(new Transformer<Context<Graph<Variable,Edge>,Edge>, Number>() {
			public Number transform(Context<Graph<Variable, Edge>, Edge> arg0) {
				return new Double(.35);
			}
		});
		vv.getRenderContext().setLabelOffset(6);
		vv.getRenderContext().setEdgeShapeTransformer(new EdgeShape.Line<Variable, Edge>());
		
		vv.getRenderer().getVertexLabelRenderer().setPosition(Position.CNTR);
		vv.getRenderer().setEdgeLabelRenderer(new PrintfEdgeLabelRenderer<Variable, Edge>());
	}
	
	public void initTextView() {
		// Log View		
		logText = new JTextPane() {
			private static final long serialVersionUID = 1L;
			public boolean getScrollableTracksViewportWidth()
		    {
		        return getUI().getPreferredSize(this).width 
		            <= getParent().getSize().width;
		    }
		};
		logText.setEditable(false);
		logText.setFont(new Font("courier new", Font.PLAIN, 14));
		logScroll = new JScrollPane(logText);
		
		logAll = new JCheckBox("All", true);
		logCall = new JCheckBox("Calls", false);
		logReturn = new JCheckBox("Returns", false);
		logIn = new JCheckBox("Scope In", false);
		logOut = new JCheckBox("Scope Out", false);
		logDecl = new JCheckBox("Declarations", false);
		logAssign = new JCheckBox("Assignments", false);
		
		logDisplayManager = new LogDisplayManager();
		logDisplayManager.setLogView(logText);
		logDisplayManager.setAllSelector(logAll);
		logDisplayManager.setFilterSelector(logCall, FuncCall.class, Color.GREEN);
		logDisplayManager.setFilterSelector(logReturn, FuncReturn.class, Color.RED);
		logDisplayManager.setFilterSelector(logIn, ScopeIn.class, Color.YELLOW);
		logDisplayManager.setFilterSelector(logOut, ScopeOut.class, Color.ORANGE);
		logDisplayManager.setFilterSelector(logDecl, VarDeclaration.class, Color.LIGHT_GRAY);
		logDisplayManager.setFilterSelector(logAssign, VarAssignment.class, Color.CYAN);
						
		logView = new JPanel();
		GroupLayout selectionLayout = new GroupLayout(logView);
		logView.setLayout(selectionLayout);
		selectionLayout.setHorizontalGroup(selectionLayout.createParallelGroup()
				.addComponent(logScroll)
				.addGroup(selectionLayout.createSequentialGroup()
						.addComponent(logAll)
						.addGroup(selectionLayout.createParallelGroup()
								.addComponent(logCall)
								.addComponent(logReturn))
						.addGroup(selectionLayout.createParallelGroup()
								.addComponent(logIn)
								.addComponent(logOut))
						.addGroup(selectionLayout.createParallelGroup()
								.addComponent(logDecl)
								.addComponent(logAssign))));
		
		selectionLayout.setVerticalGroup(selectionLayout.createSequentialGroup()
				.addComponent(logScroll)
				.addGroup(selectionLayout.createParallelGroup()
						.addComponent(logAll)
						.addComponent(logCall)
						.addComponent(logIn)
						.addComponent(logDecl))
				.addGroup(selectionLayout.createParallelGroup()
						.addComponent(logReturn)
						.addComponent(logOut)
						.addComponent(logAssign)));
		
		// Source View
		sourceTabs = new JTabbedPane(JTabbedPane.TOP, JTabbedPane.SCROLL_TAB_LAYOUT);
		setSource = new JButton("Set Source Root");
		setSource.setEnabled(false);
		setSource.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				selectSourceRoot();
			}
		});
		
		sourceView = new JPanel();
		GroupLayout sourceLayout = new GroupLayout(sourceView);
		sourceView.setLayout(sourceLayout);
		sourceLayout.setHorizontalGroup(sourceLayout.createParallelGroup()
				.addComponent(sourceTabs)
				.addComponent(setSource)
				);
		
		sourceLayout.setVerticalGroup(sourceLayout.createSequentialGroup()
				.addComponent(sourceTabs)
				.addComponent(setSource)
				);
		
		textView = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, logView, sourceView);
		textView.setOneTouchExpandable(true);
	}
	
	public void initMenus() {
		menuBar = new JMenuBar();
		mnuFile = new JMenu("File");
		mnuFile.setMnemonic(KeyEvent.VK_F);
		itemOpenLog = new JMenuItem("Open Log", KeyEvent.VK_O);
		itemOpenLog.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				int result = logChooser.showOpenDialog(Visualizer.this);
				if (result == JFileChooser.APPROVE_OPTION) {
					loadLog(logChooser.getSelectedFile());
				}
			}
		});
		mnuFile.add(itemOpenLog);
		/*itemSetSourceRoot = new JMenuItem("Set Source Root", KeyEvent.VK_R);
		itemSetSourceRoot.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				selectSourceRoot();
			}
		});
		mnuFile.add(itemSetSourceRoot);*/
		mnuFile.add(new JSeparator());
		itemExit = new JMenuItem("Exit", KeyEvent.VK_X);
		itemExit.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				dispose();
			}
		});
		mnuFile.add(itemExit);
		menuBar.add(mnuFile);
		
		
		mnuView = new JMenu("View");
		mnuView.setMnemonic('v');
		itemTransformMode = new JMenuItem("Transform Mode", KeyEvent.VK_T);
		itemTransformMode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				gm.setMode(ModalGraphMouse.Mode.TRANSFORMING);
			}
		});
		mnuView.add(itemTransformMode);
		itemPickingMode = new JMenuItem("Picking Mode", KeyEvent.VK_P);
		itemPickingMode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				gm.setMode(ModalGraphMouse.Mode.PICKING);
			}
		});
		mnuView.add(itemPickingMode);
		menuBar.add(mnuView);
		
		mnuHelp = new JMenu("Help");
		mnuHelp.setMnemonic(KeyEvent.VK_H);
		itemAbout = new JMenuItem("About", KeyEvent.VK_A);
		itemAbout.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				JOptionPane.showMessageDialog(Visualizer.this, "SpokenC: The visual printf debugger.", "About", JOptionPane.WARNING_MESSAGE);
			}
		});
		mnuHelp.add(itemAbout);
		menuBar.add(mnuHelp);
		
		logChooser = new JFileChooser(new File("C:\\Users\\Andrew\\Programming\\Java Projects\\CS171\\logs"));
		FileNameExtensionFilter logFilter = new FileNameExtensionFilter("log files", "log");
		logChooser.setFileFilter(logFilter);
		logChooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
		logChooser.setMultiSelectionEnabled(false);
		
		sourceChooser = new JFileChooser(new File("C:\\Users\\Andrew\\Programming\\Java Projects\\CS171\\logs"));
		sourceChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
		logChooser.setMultiSelectionEnabled(false);
	}
	
	public void loadLog(File logFile) {
		Log newLog = LogParser.ParseLog(logFile);
		if (newLog != null) {
			Variable.NumDecls = 0;
			Variable.NumLines = 0;
			log = newLog;
			graph = buildGraph(log);
			layout.setGraph(graph);
			vv.repaint();
			
			logDisplayManager.setLog(log);
			loadSourceView();
			setSource.setEnabled(true);
		} else {
			JOptionPane.showMessageDialog(this, "Could not open selected log file. May not be the correct format.",
					"Error loading log", JOptionPane.ERROR_MESSAGE);
		}
	}
	
	public Graph<Variable, Edge> buildGraph(Log log) {
		Graph<Variable, Edge> graph = new DirectedSparseGraph<>();
		Stack<FunctionScope> callStack = new Stack<>();
		
		for (LogEntry entry : log.getLogItems()) {
			if (entry instanceof FuncCall) {
				FuncCall call = (FuncCall)entry;
				callStack.push(new FunctionScope(call.getFuncName()));
			} else if (entry instanceof FuncReturn) {
				callStack.pop();
			} else if (entry instanceof ScopeIn) {
				callStack.peek().scopeIn();
			} else if (entry instanceof ScopeOut) {
				callStack.peek().scopeOut();
			} else if (entry instanceof VarDeclaration) {
				VarDeclaration decl = (VarDeclaration)entry;
				Variable v = new Variable(decl.getValue(), callStack.peek().getName());
				
				callStack.peek().addVariable(v);
				
				v.setCallStack(callStackString(callStack));
				
				graph.addVertex(v);
			} else if (entry instanceof VarAssignment) {
				VarAssignment assign = (VarAssignment)entry;
				Variable prev = callStack.peek().getVariable(assign.getValue().getName());
				Variable next = new Variable(assign.getValue(), callStack.peek().getName(), prev.getDeclNum());
				
				callStack.peek().updateVariable(next);
				
				next.setCallStack(callStackString(callStack));
				
				graph.addVertex(next);
				graph.addEdge(new Edge(assign.getLocation()), prev, next);
			}
		}
		
		return graph;
	}
	
	private StyledDocument callStackString(Stack<FunctionScope> callStack) {
		FunctionScope frames[] = new FunctionScope[callStack.size()];
		frames = callStack.toArray(frames);
		
		StyledDocument stack = new DefaultStyledDocument();
		for (int i = frames.length - 1; i >= 0; i--) {
			frames[i].appendToStyledDocument(stack, getColorFromFunction(frames[i].getName()));
		}
		return stack;
	}

	private void selectSourceRoot() {
		int result = sourceChooser.showOpenDialog(Visualizer.this);
		if (result == JFileChooser.APPROVE_OPTION) {
			loadSourceView();
		}
	}
	
	public void loadSourceView() {
		if (log == null) {
			return;
		}
		sourceTabs.removeAll();
		Set<String> files = new HashSet<>();
		for (LogEntry entry : log.getLogItems()) {
			if (!files.contains(entry.getFileName())) {
				files.add(entry.getFileName());
				JTextArea source = new JTextArea();
				source.setTabSize(2);
				source.setEditable(false);
				JScrollPane scroll = new JScrollPane(source);
				
				File sourceFile;
				if (sourceChooser.getSelectedFile() != null) {
					sourceFile = new File(sourceChooser.getSelectedFile().getAbsolutePath() + "/" + entry.getFileName());
				} else {
					sourceFile = new File(sourceChooser.getCurrentDirectory().getAbsoluteFile() + "/" + entry.getFileName());
				}
				String s = "";
				BufferedReader in;
				try {
					in = new BufferedReader(new FileReader(sourceFile));
					String line;
					try {
						int lineNum = 0;
						JTextArea lineNums = new JTextArea();
						lineNums.setEditable(false);
						while ((line = in.readLine()) != null) {
							s += line + "\n";
							lineNums.append(++lineNum + ":\n");
						}
						scroll.setRowHeaderView(lineNums);
					} catch (IOException e) {
						source.setText("Cannot read source file.");
						//e.printStackTrace();
					}
					source.setText(s);
				} catch (FileNotFoundException e1) {
					source.setText("Source file not found.");
					//e1.printStackTrace();
				}
				sourceTabs.add(entry.getFileName(), scroll);
			}
		}
	}
	
	public static void main(String[] args) {
        try {
			UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
		} catch (ClassNotFoundException | InstantiationException
				| IllegalAccessException | UnsupportedLookAndFeelException e) {
			e.printStackTrace();
		}
		new Visualizer();
	}
}
