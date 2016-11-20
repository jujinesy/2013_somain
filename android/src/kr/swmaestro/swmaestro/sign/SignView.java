package kr.swmaestro.swmaestro.sign;

import java.io.File;
import java.io.FileOutputStream;
import java.util.ArrayList;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.os.Environment;
import android.util.AttributeSet;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup.LayoutParams;
import android.widget.Toast;

public class SignView extends View {
	private Context mContext;
	ArrayList<Point> points = new ArrayList<Point>();

	public SignView(Context context, AttributeSet attrs, int defStyleAttr) {
		super(context, attrs, defStyleAttr);
		init(context);
	}
	public SignView(Context context, AttributeSet attrs) {
		super(context, attrs);
		init(context);
	}
	public SignView(Context context) {
		super(context);
		init(context);
	}

	private void init(Context context){
		mContext= context;
		setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT));
		this.setOnTouchListener(new OnTouchListener() {
			@Override
			public boolean onTouch(View v, MotionEvent event) {
				switch( event.getAction() ) {
				case MotionEvent.ACTION_MOVE:
					points.add(new Point(event.getX(), event.getY(), true));
					invalidate();
					break;
				case MotionEvent.ACTION_UP:
				case MotionEvent.ACTION_DOWN: 
					points.add(new Point(event.getX(), event.getY(), false));
				}
				return true;
			}
		});
	}

	public void clear(){
		points.clear();
		invalidate();
	}

	@Override
	protected void onDraw(Canvas canvas) {
		super.onDraw(canvas);
		Paint p = new Paint();
		p.setColor(Color.BLACK);
		p.setStrokeWidth(10);
		for(int i=1; i<points.size(); i++) {
			if(!points.get(i).isDraw) continue;
			canvas.drawLine(points.get(i-1).x, points.get(i-1).y, points.get(i).x, points.get(i).y, p);
		}
	}

	class Point {
		float x;
		float y;
		boolean isDraw;
		public Point(float x, float y, boolean isDraw) {
			this.x = x;
			this.y = y;
			this.isDraw = isDraw;
		}
	}

	public boolean saveView(String fileName) {
		try{
			View view = this;
			String path = Environment.getExternalStorageDirectory().getAbsolutePath();
			Bitmap  b = Bitmap.createBitmap(view.getWidth(), view.getHeight(), Bitmap.Config.RGB_565);

			if(b!=null){
				try { 
					File f = new File(path+"/somain");
					f.mkdir();
					File f2 = new File(path + fileName);

					Canvas c = new Canvas(b);
					c.drawColor(Color.WHITE);
					view.draw(c); 
					FileOutputStream fos = new FileOutputStream(f2);

					if (fos != null){ 
						b.compress(Bitmap.CompressFormat.PNG, 100, fos ); 
						fos.close(); 
					}
				} catch( Exception e ){ 
					Log.e("testSaveView", "Exception: " + e.toString() ); 
				} 
			}
//			Toast.makeText(mContext, "서명이 저장되었습니다", Toast.LENGTH_SHORT).show();
			return true;
		} catch(Exception e){
//			Toast.makeText(mContext, "서명이 저장에 실패했습니다", Toast.LENGTH_SHORT).show();
			return false;
		}
	}  
}