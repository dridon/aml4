import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Collections;
import java.util.Scanner;
import java.util.AbstractList;

import java.util.ArrayList;




public class LibraryFileManager {
	
	protected String inFileName;
	protected String outFileName;
	protected String fileSep; 
	protected int numInputs;
	private ArrayList<Book> fileContents;
	protected double[] answers;
	double [][] normBooks;
	PrintWriter outstream;
	
	public LibraryFileManager(String pInFilename,String pOutFilename,String pFilesep)
	{
		inFileName = pInFilename;
		outFileName = pOutFilename;
		fileSep = pFilesep;
		numInputs = 0;
		fileContents = null;
		answers = null;
		outstream = null;
		normBooks = null;
	}
	
	public ArrayList<Book> readInputs(boolean inHeader)
	{
		fileContents = new ArrayList<Book>();
		Scanner inputStream = null;
		try{
			File f = new File(inFileName);
			inputStream = new Scanner(f);
			if (inHeader)
				inputStream.nextLine();
			boolean moreInput = true;
			String line = inputStream.nextLine();
			String[] values = line.split(fileSep);
			System.out.println("reading input file");
			numInputs = values.length;
			while(moreInput)
			{
				if (values.length != 5)
					System.out.println(line);
				Book theBook = new Book(values);
				fileContents.add(theBook);
				if(inputStream.hasNext())
				{
					line = inputStream.nextLine();
					values = line.split(fileSep);
				}
				else
					moreInput = false;
			}
			inputStream.close();
			System.out.println("read "+fileContents.size()+" records");
		}
		catch (FileNotFoundException|NumberFormatException e)
		{
			e.printStackTrace();
		}
		finally
		{
			if(inputStream != null)
				inputStream.close();
		}
		return fileContents;
	}		
	public double[] readOutputs(boolean header)
	{
		System.out.println("reading answer file "+outFileName);
		answers = new double[fileContents.size()];
		Scanner inputStream = null;
		try
		{
			File f = new File(outFileName);
			inputStream = new Scanner(f);
			if(header)
			{
				String line = inputStream.nextLine();//skip header
			}
			int i = 0;
			while(inputStream.hasNext())
			{
				answers[i++] = Double.parseDouble(inputStream.nextLine());
			}
			System.out.println("read "+i+" records");
			assert i == fileContents.size();
		}
		catch (FileNotFoundException|NumberFormatException e)
		{
			e.printStackTrace();
		}
		finally
		{
			if(inputStream != null)
				inputStream.close();
		}
		
		return answers;
	}
	
	public int getNumInputs()
	{
		return numInputs;
	}
	
	
}
