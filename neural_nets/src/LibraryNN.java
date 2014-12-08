import org.encog.Encog;
import org.encog.engine.network.activation.ActivationTANH;
import org.encog.ml.data.MLData;
import org.encog.ml.data.MLDataPair;
import org.encog.ml.data.MLDataSet;
import org.encog.ml.data.basic.BasicMLDataSet;
import org.encog.neural.networks.BasicNetwork;
import org.encog.neural.networks.layers.BasicLayer;
import org.encog.neural.networks.training.propagation.resilient.*;
import org.encog.persist.EncogDirectoryPersistence;

import java.util.Random;
import java.util.AbstractList;
import java.util.ArrayList;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Scanner;

public class LibraryNN {

	public static String path = "/Users/Fernando1/Documents/grad/COMP 598 Machine Learning/project 4/nn files/";
	public static final boolean FROM_SCRATCH = true;
	public static final String WEIGHT_FILE = "Outremont-weights.eg";
	//public static final String SAVE_TO_FILE = FILE_PRE+"weights.eg";
	public static final String[]libraries = {"Plateau-M","Rosemont ",
											"Saint-Lau","Anjou","Mercier-"};

	public static final int NUM_FOLDS = 4;
	public static final int NUM_OUTPUTS = 1;
	public static final int NUM_HIDDEN = 4;
	public static final boolean NORM_OUTPUT = false;
	public static final double MIN_CHANGE= 1E-7;
	public static final double ERROR = .1;
	public static final int LOWER = 1;
	public static final int DISPL_THRESHOLD = 10000;
	public static final int SAVE_THRESHOLD = 500;
	public static Random rand = new Random();

	protected MLDataSet createMLDataSet(AbstractList<Book> books, AbstractList<Double> answers)
	{
		assert books.size() == answers.size();
		double x[][] = new double[books.size()][Book.numFields];
		double d[][] = new double[books.size()][1];
		int i = 0;
		for(Book b: books)
		{
			x[i] = b.normalize();
			d[i][0] = answers.get(i);
			i++;
		}

		return new BasicMLDataSet(x,d);
	}
	public double classify(String branch,int fold, AbstractList<Book> trainIn, AbstractList<Double> trainOut, AbstractList<Book> validIn, AbstractList<Double>validOut) {
		int numInputs = Book.numFields;
		double accuracy = 0.0;
		BasicNetwork network = null;
		if(FROM_SCRATCH)
		{	
			// create a neural network, without using a factory
			network = new BasicNetwork();
			network.addLayer(new BasicLayer(new ActivationTANH(),true,numInputs));
			network.addLayer(new BasicLayer(new ActivationTANH(),true,NUM_HIDDEN));
			network.addLayer(new BasicLayer(new ActivationTANH(),true,NUM_HIDDEN/2));
			network.addLayer(new BasicLayer(new ActivationTANH(),false,NUM_OUTPUTS));
			network.getStructure().finalizeStructure();
			network.reset();
		}
		else
		{	
			network = (BasicNetwork)EncogDirectoryPersistence.loadObject(new File(path+WEIGHT_FILE));
		}
		
		MLDataSet trainingSet = createMLDataSet(trainIn, trainOut);

		// train the neural network
		System.out.println("-----------TRAINING NEURAL NETWORK------------");
		final ResilientPropagation train = new ResilientPropagation(network, trainingSet);
		int epoch = 0;
		double oldError = 0.0,
				newError = ERROR+1;
		boolean keepTraining = true;

		while(keepTraining && newError > ERROR)
		{

			if(epoch % DISPL_THRESHOLD == 0)
			{
				keepTraining = (Math.abs(newError - oldError) > MIN_CHANGE /*&& newError <= oldError*/);
				oldError = newError;
				System.out.println("Epoch #" + epoch + " Error:" + train.getError());
			}
			/*if(epoch % SAVE_THRESHOLD == 1) //compare to 1 because do not want it to save at first iteration
					EncogDirectoryPersistence.saveObject(new File(FILE_PRE+SAVE_TO_FILE), network);*/
			train.iteration();			
			epoch++;
			newError = train.getError();
		}
		System.out.println("final error: "+newError+" at epoch " +epoch);
		train.finishTraining();
		File f = new File(path+branch+"weights"+fold+".eg");
		if(!f.exists()) {
			try
			{
				f.createNewFile();
			}
			catch (IOException e)
			{
				e.printStackTrace();
			}
		} 
		EncogDirectoryPersistence.saveObject(f, network);

		// test the neural network
		MLDataSet testingSet = createMLDataSet(validIn, validOut);
		PrintWriter outstream = null;
		try{
			File testfile = new File(path+branch+"-results.csv");
			outstream = new PrintWriter(testfile);

			System.out.println("Neural Network Test Results:");
			outstream.write("test,actual,correct,isError");

			int numErrors =0;
			int numSuccess =0;
			int testNo =0;
			int truePos = 0;
			int trueNeg = 0;
			int totPos = 0;
			int totNeg = 0;
			for(MLDataPair pair : testingSet) {
				testNo++;
				double answer = pair.getIdeal().getData(0);
				if(Math.round(answer) == 0)
				{
					totNeg++;
				}
				else
					totPos++;
			
				final MLData output = network.compute(pair.getInput());
				if(Math.round(output.getData(0)) != pair.getIdeal().getData(0))
				{
					numErrors++;
				}
				else
				{
					numSuccess++;
					if (Math.round(answer) == 0)
						trueNeg++;
					else
						truePos++;
				}

				outstream.write("test "+testNo
						+ "," + output.getData(0)  
						+ "," + pair.getIdeal().getData(0) 
						+ "," + (Math.round(output.getData(0)) == pair.getIdeal().getData(0))
						+"\n");
			}
			System.out.println("Number errors: "+numErrors);
			System.out.print("Accuracy: ");
			accuracy = (float)(numSuccess)/testingSet.getRecordCount() *100;
			double sens = (float)truePos/totPos;
			double spec = (float)trueNeg/totNeg;
			System.out.println(accuracy+" sensitivity "+ sens+" specificity "+spec);
			
		}
		catch (IOException e)
		{
			System.err.println(e);
		}
		finally
		{
			Encog.getInstance().shutdown();
			if(outstream != null)
				outstream.close();
		}
		return accuracy;
	}

	public static void main(String[] args) {
		for(String branch: libraries)
		{
			LibraryFileManager trainLFM = new LibraryFileManager(path+branch+"-train_inputs.csv",path+branch+"-train_outputs.csv",",");
			ArrayList<Book> books = trainLFM.readInputs(false);
			double[] answers = trainLFM.readOutputs(false);
			int validSize = books.size()/NUM_FOLDS;
			int trainSize = books.size() - validSize;
			for(int fold=0; fold<NUM_FOLDS;fold++)
			{
				AbstractList<Book> trainIn = new ArrayList<Book>();
				AbstractList<Double> trainOut = new ArrayList<Double>();
				AbstractList<Book> validIn = new ArrayList<Book>();
				AbstractList<Double> validOut = new ArrayList<Double>();
				int i = 0;
				for (Book b: books)
				{
					if(i%NUM_FOLDS != fold)
					{	
						trainIn.add(b);
						trainOut.add(answers[i]);
					}
					else
					{
						validIn.add(b);
						validOut.add(answers[i]);
					}
					i++;
				}
				LibraryNN lnn = new LibraryNN();
				double result = lnn.classify(branch,fold,trainIn,trainOut,validIn,validOut);
				System.out.println(branch+" fold "+fold+" result: "+result);
			}
		}
	}

}