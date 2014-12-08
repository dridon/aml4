

public class Book {
	static protected int numFields = 2;
	static private int maxPosCirc = 0;
	static private int maxNegCirc = 0;
	private Double callNo;
	private int authPosCirc;
	private int authNegCirc;
	private int year;
	private int lang;
	
	public Book(String[] values) {
		this.callNo = Double.valueOf(values[0]);
		this.authPosCirc = Integer.valueOf(values[1]);
		if(authPosCirc > maxPosCirc)
		{
			maxPosCirc = authPosCirc;
		}
		this.authNegCirc = Integer.valueOf(values[2]);
		if(authNegCirc > maxNegCirc)
		{
			maxNegCirc = authNegCirc;
		}
		this.year = Integer.valueOf(values[3]);
		this.lang = Integer.valueOf(values[4]);
	}

	public double getCallNo() {
		return callNo;
	}

	public int getAuthPosCirc() {
		return authPosCirc;
	}

	public int getAuthNegCirc() {
		return authNegCirc;
	}

	public int getYear() {
		return year;
	}

	public int getLang() {
		return lang;
	}
	
	public String toString(char sep)
	{
		return new String(callNo.toString() + sep + authPosCirc + sep 
						+ authNegCirc + sep + year + sep + lang);
	}
	
	public double[] normalize()
	{
		double[] output = new double[numFields];
		output[0]=callNo / 1000.0;
		//output[1]=authPosCirc/maxPosCirc;
		//output[2]=authNegCirc/maxNegCirc;
		output[1]=year/2014.0;
		//output[4]=lang;
		return output;
	}
}
