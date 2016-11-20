package kr.swmaestro.swmaestro.notice;

import java.util.ArrayList;

import kr.swmaestro.swmaestro.R;
import kr.swmaestro.swmaestro.data.DataNotice;
import kr.swmaestro.swmaestro.other.Pref;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.view.Window;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ListView;

public class NoticeListActivity extends ActionBarActivity implements OnItemClickListener{
	private String TAG = this.getClass().getSimpleName();
	private Context mContext;
	
	private ListView lv;
	private NoticeListAdapter mNoticeListAdapter;
	private ArrayList<DataNotice> mDataNoticeList;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		requestWindowFeature(Window.FEATURE_NO_TITLE);
		setContentView(R.layout.notice_list);
		mContext = this;
		
		mDataNoticeList = Pref.getDataNoticeList(mContext);
		lv = (ListView) findViewById(R.id.lvNoticeList);
		mNoticeListAdapter = new NoticeListAdapter(mContext, R.layout.notice_list_listitem, mDataNoticeList);
		lv.setAdapter(mNoticeListAdapter);
		
		lv.setOnItemClickListener(this);
	}

	@Override
	public void onItemClick(AdapterView<?> adapter, View v, int position, long id) {
		Intent intent = new Intent(NoticeListActivity.this, NoticeActivity.class);
		intent.putExtra("position", position);
		startActivity(intent);
	}

}
