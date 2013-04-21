package cs171.printf;

import java.awt.Dimension;
import java.awt.geom.Point2D;
import java.awt.Point;

import org.apache.commons.collections15.Transformer;

import cs171.printf.environment.Edge;
import cs171.printf.environment.Variable;

import edu.uci.ics.jung.algorithms.layout.Layout;
import edu.uci.ics.jung.graph.Graph;

public class PrintfLayout implements Layout<Variable, Edge> {
	
	protected Graph<Variable, Edge> graph;
	protected Dimension dimension;
	protected Transformer<Variable, Point2D> transformer;
	
	public PrintfLayout(Graph<Variable, Edge> graph) {
		this.graph = graph;
		transformer = new Transformer<Variable, Point2D>() {
			public Point2D transform(Variable variable) {
				int xDelta = 100;//(int)(dimension.getWidth() / (Variable.NumDecls + 1));
				int yDelta = 40;//(int)(dimension.getHeight() / (Variable.NumLines + 2));
				return new Point(xDelta * variable.getDeclNum() + xDelta / 2, yDelta * variable.getLogLine() + yDelta / 2);
			}
		};
	}

	public Point2D transform(Variable variable) {
		return transformer.transform(variable);
	}

	public Graph<Variable, Edge> getGraph() {
		return graph;
	}

	public Dimension getSize() {
		return dimension;
	}

	public void initialize() {
		// TODO Auto-generated method stub
		
	}

	public boolean isLocked(Variable arg0) {
		// TODO Auto-generated method stub
		return false;
	}

	public void lock(Variable arg0, boolean arg1) {
		// TODO Auto-generated method stub
		
	}

	public void reset() {
		// TODO Auto-generated method stub
		
	}

	public void setGraph(Graph<Variable, Edge> graph) {
		this.graph = graph;
	}

	public void setInitializer(Transformer<Variable, Point2D> transformer) {
		this.transformer = transformer;
	}

	public void setLocation(Variable arg0, Point2D arg1) {
		// TODO Auto-generated method stub
		
	}

	public void setSize(Dimension dimension) {
		this.dimension = dimension;
	}
}
