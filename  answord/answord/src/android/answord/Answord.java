package android.answord;

import android.app.Activity;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.AdapterView.OnItemSelectedListener;

public class Answord extends Activity {
    /** Called when the activity is first created. */
	Spinner books_spinner;
	Spinner chapters_spinner;
	TextView currentview;
	String cbook;
	int cchapter=1;
	private SQLiteDatabase myDB = null;
	@Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        books_spinner = (Spinner)findViewById(R.id.books);
        String[] books = getBooks();
        ArrayAdapter<String> books_adapter = new ArrayAdapter<String>(this,android.R.layout.simple_spinner_item,books);
        books_adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        books_spinner.setAdapter(books_adapter);
        books_spinner.setOnItemSelectedListener(new Spinner.OnItemSelectedListener(){
        	@Override
			public void onItemSelected(AdapterView<?> parent, View v,
					int position, long id) {
        		cbook = (String)parent.getAdapter().getItem(position);
        		chapters_spinner.setAdapter(generateChapters(cbook));
			}
			@Override
			public void onNothingSelected(AdapterView<?> arg0) {
				// TODO Auto-generated method stub
				
			}
        	
        });
        chapters_spinner = (Spinner) findViewById(R.id.chapters);
        chapters_spinner.setOnItemSelectedListener(new Spinner.OnItemSelectedListener(){
        	@Override
			public void onItemSelected(AdapterView<?> parent, View v,
					int position, long id) {
        		cchapter= position+1;
        		currentview.setText(getChapter(cbook,cchapter));
			}
			@Override
			public void onNothingSelected(AdapterView<?> arg0) {
				// TODO Auto-generated method stub
				
			}
        	
        });
        currentview = (TextView)this.findViewById(R.id.currentview);
    }
	public ArrayAdapter<Integer> generateChapters(String book ){
		openDB();
		Cursor c = myDB.rawQuery("SELECT max(chapter) FROM bbe WHERE book ='"+book+"'", null);
		c.moveToFirst();
		int end  = c.getInt(0);
		closeDB(); 
		Integer[] chapters = new Integer[end];
        for(int i =0;i<chapters.length;i++){
        	chapters[i] = new Integer(i+1);
        }
        ArrayAdapter<Integer> chapters_adapter = new ArrayAdapter<Integer>(this,android.R.layout.simple_spinner_item,chapters);
        chapters_adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        return chapters_adapter;
	}
	public String getChapter(String book,int chapter){
		StringBuilder b = new StringBuilder();
		openDB();
		String q = "SELECT verse,scripture from bbe WHERE book = '"+book+"' AND chapter='"+chapter+"'";
		Cursor c = myDB.rawQuery(q, null);
		c.moveToFirst();
		while(!c.isAfterLast()){
			int verse = c.getInt(0);
			String scripture = c.getString(1);
			b.append(chapter+":"+verse+" "+scripture+"\n");
			c.moveToNext();
		}
		return b.toString();
	}
	public String[] getBooks(){
		String[] books = {};
		openDB();
		if(myDB != null){
			Cursor c = myDB.rawQuery("SELECT DISTINCT book FROM bbe ORDER BY id", null);
			int count = c.getCount();
			books = new String[count];
			c.moveToFirst();
			for(int i=0;i<count;i++){
				books[i] = c.getString(0);
				c.moveToNext();		
			}
		}
		closeDB();
		return books;
		
	}
	public void openDB(){
		try{
			myDB = SQLiteDatabase.openDatabase("/sdcard/bibloid/bibles/bbe.db",null,SQLiteDatabase.NO_LOCALIZED_COLLATORS);
		}catch(Exception e){
			Log.e("BIBLOID", e.getMessage());
		}
	}
	public void closeDB(){
		if(myDB.isOpen()){
			myDB.close();
		}
	}

}
