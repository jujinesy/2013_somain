package kr.swmaestro.swmaestro.document;

import java.util.ArrayList;

import kr.swmaestro.swmaestro.R;
import kr.swmaestro.swmaestro.data.DataDocument;
import kr.swmaestro.swmaestro.data.DataUser;
import kr.swmaestro.swmaestro.other.C;
import kr.swmaestro.swmaestro.other.Pref;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.widget.AdapterView;
import android.widget.FrameLayout;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ListView;

public class DocumentListActivity extends ActionBarActivity implements OnItemClickListener{
	private String TAG = this.getClass().getSimpleName();
	private Context mContext;

	private ListView lv;
	private FrameLayout flBar;

	private ArrayList<DataDocument> mDocumentList;
	private DocumentListAdapter mAdapter;
	private int resDocumentList;

	private String type;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		requestWindowFeature(Window.FEATURE_NO_TITLE);
		setContentView(R.layout.document_list);
		mContext = this;

		lv = (ListView) findViewById(R.id.lvDocumentList);
		flBar = (FrameLayout) findViewById(R.id.flDocumentListBar);

		Intent intent = getIntent();
		type = intent.getStringExtra("type");
		if(type.equals("unsigned")){
			resDocumentList = R.layout.document_list_listitem_unsigned;
			flBar.setBackgroundResource(R.drawable.sign_bar);
		} else if(type.equals("signed")){
			resDocumentList = R.layout.document_list_listitem_signed;
		}

		mDocumentList = Pref.getDataDocumentList(mContext, type);
		mAdapter = new DocumentListAdapter(mContext, resDocumentList, mDocumentList);
		lv.setAdapter(mAdapter);
		lv.setOnItemClickListener(this);
	}

	@Override
	public void onItemClick(AdapterView<?> adapter, View v, int position, long id) {
		DataDocument selectedDataDocument = mDocumentList.get(position);
		Intent intent = null;
		intent = new Intent(DocumentListActivity.this, DocumentActivity.class);
		intent.putExtra("type", type);
		intent.putExtra("document_id", selectedDataDocument.getDocumentId());
		startActivityForResult(intent, C.ACTIVITY_DOCUMENT);
	}

	@Override
	protected void onResume() {
		super.onResume();
//		Log.d(TAG, "onResume");
//		mDocumentList = Pref.getDataDocumentList(mContext, type);
//		Log.d(TAG, "mDocumentList Size : " + mDocumentList.size());
//		mAdapter.notifyDataSetChanged();
	}
	
	

	@Override
	protected void onActivityResult(int requestCode, int resultCode, Intent data) {
		if(resultCode == RESULT_OK){
			new DocumentListRefreshTask(mContext, "문서목록 다시 불러오는 중...", type).execute();
		}
	}



	// 데이터 다시 받아온 뒤 리스트 Refresh
	class DocumentListRefreshTask extends DocumentListBaseTask {
		public DocumentListRefreshTask(Context context, String title, String type) {
			super(context, title, type);
		}

		@Override
		protected void onPostExecute(Integer result) {
			super.onPostExecute(result);
			Pref.setDataDocumentString(mContext, resultString, type);
			mDocumentList.clear();
			Log.d(TAG, "DocumentListActivity - mDocumentList Size : " + mDocumentList.size());
			mAdapter.notifyDataSetChanged();
			mDocumentList = Pref.getDataDocumentList(mContext, type);
			Log.d(TAG, "DocumentListActivity - mDocumentList Size : " + mDocumentList.size());
			mAdapter = new DocumentListAdapter(mContext, resDocumentList, mDocumentList);
			lv.setAdapter(mAdapter);
		}	
	}

}
