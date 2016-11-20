package kr.swmaestro.swmaestro.notice;

import kr.swmaestro.swmaestro.R;
import kr.swmaestro.swmaestro.data.DataNotice;
import kr.swmaestro.swmaestro.other.Pref;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.Window;
import android.webkit.WebView;
import android.widget.TextView;

public class NoticeActivity extends ActionBarActivity {
	private String TAG = this.getClass().getSimpleName();
	private Context mContext;
	
	private TextView tvCategory, tvTitle, tvDate; 
	private WebView wv;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		requestWindowFeature(Window.FEATURE_NO_TITLE);
		setContentView(R.layout.notice);
		mContext = this;
		
		tvCategory = (TextView) findViewById(R.id.tvNoticeCategory);
		tvTitle = (TextView) findViewById(R.id.tvNoticeTitle);
		tvDate = (TextView) findViewById(R.id.tvNoticeDate);
		
		Intent intent = getIntent();
		int position = intent.getIntExtra("position", 0);
		DataNotice dataNotice = Pref.getDataNoticeList(mContext).get(position);
		
		tvCategory.setText(dataNotice.getCategory());
		tvTitle.setText(dataNotice.getTitle());
		tvDate.setText(dataNotice.getCreatedDate());
		
		Log.d(TAG, "getContent:" + dataNotice.getContent());
		String summary = "<meta http-equiv='Content-Type' content='text/html; charset=utf-16le'>" +
	            "<html>" +
	             "<body style='font-size: 9pt;'>" +
	            dataNotice.getContent() +
	            "</body>" +
	            "</html>";
		
		Log.d(TAG, "summary:" + summary);
		
		wv = (WebView) findViewById(R.id.wvNotice);
		wv.getSettings().setDefaultTextEncodingName("UTF-8");
		wv.loadData(summary, "text/html; charset=UTF-8", null);
	}	
}
