package kr.swmaestro.swmaestro.document;

import java.util.ArrayList;

import kr.swmaestro.swmaestro.R;
import kr.swmaestro.swmaestro.data.DataDocument;
import kr.swmaestro.swmaestro.data.DataDocumentExtend;
import kr.swmaestro.swmaestro.data.DataUser;
import kr.swmaestro.swmaestro.other.C;
import kr.swmaestro.swmaestro.other.CommonFunction;
import kr.swmaestro.swmaestro.other.Pref;
import kr.swmaestro.swmaestro.sign.SignActivity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.Window;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

public class DocumentActivity extends ActionBarActivity implements OnClickListener {
	private String TAG = this.getClass().getSimpleName();
	private Context mContext;

	private ListView lv;
	private DocumentAdapter mAdapter;
	private View viewHeader;
	private TextView tvType, tvDeadline, tvSignUsers, tvSignedUsers, tvIsSubmitted, tvIsComplete, tvSubmituser;
	private Button btnSign;

	private DataDocument mDataDocument;
	private ArrayList<DataDocumentExtend> mDataDocumentExtendList;
	private int position;
	private String type;
	private int documentId;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		requestWindowFeature(Window.FEATURE_NO_TITLE);
		setContentView(R.layout.document);
		mContext = this;

		lv = (ListView) findViewById(R.id.lvDocument);

		Intent intent = getIntent();
//		position = intent.getIntExtra("position", 0);
		documentId = intent.getIntExtra("document_id", -1);
		type = intent.getStringExtra("type");

		mDataDocument = Pref.getDataDocument(mContext, type, documentId);
		
		// Header Set
		LayoutInflater inflater = (LayoutInflater) mContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		viewHeader = inflater.inflate(R.layout.document_header, null);

		tvType = (TextView) viewHeader.findViewById(R.id.tvDocumentType);
		tvDeadline = (TextView) viewHeader.findViewById(R.id.tvDocumentDeadline);
		tvSignUsers = (TextView) viewHeader.findViewById(R.id.tvDocumentSignUsers);
		tvSignedUsers = (TextView) viewHeader.findViewById(R.id.tvDocumentSignedUsers);
		tvIsSubmitted = (TextView) viewHeader.findViewById(R.id.tvDocumentIsSubmitted);
		tvIsComplete = (TextView) viewHeader.findViewById(R.id.tvDocumentIsComplete);
		tvSubmituser = (TextView) viewHeader.findViewById(R.id.tvDocumentSubmitUser);
		btnSign = (Button) findViewById(R.id.btnDocumentSign);


		tvType.setText(mDataDocument.getDocumentType());
		tvDeadline.setText(mDataDocument.getDeadLine());
		tvSignUsers.setText(CommonFunction.getUserListString(mDataDocument.getSignUserList()));
		tvSignedUsers.setText(CommonFunction.getUserListString(mDataDocument.getSignedUserList()));
		tvIsSubmitted.setText(Boolean.toString(mDataDocument.isSubmitted()));
		tvIsComplete.setText(Boolean.toString(mDataDocument.isComplete()));
		DataUser submitUser = mDataDocument.getSubmitUser();
		if(submitUser != null){
			tvSubmituser.setText(submitUser.getName());	
		}
		btnSign.setOnClickListener(this);

		// ListView 세팅
		lv.addHeaderView(viewHeader);
		mDataDocumentExtendList = mDataDocument.getDocumentExtendList();
		mAdapter = new DocumentAdapter(mContext, android.R.layout.simple_list_item_1, mDataDocumentExtendList);
		lv.setAdapter(mAdapter);

		if(mDataDocument.isSubmitted() == true){
			btnSign.setVisibility(View.GONE);
		}
	}

	@Override
	public void onClick(View v) {
		switch(v.getId()){
		case R.id.btnDocumentSign:
			Intent intent = new Intent(DocumentActivity.this, SignActivity.class);
			intent.putExtra("document_id", documentId);
			intent.putExtra("document_type", mDataDocument.getDocumentType());
			intent.putExtra("document_deadline", mDataDocument.getDeadLine());
			startActivityForResult(intent, C.ACTIVITY_SIGN);
			break;
		}
	}

	@Override
	protected void onActivityResult(int requestCode, int resultCode, Intent data) {
		super.onActivityResult(requestCode, resultCode, data);
		if(resultCode == RESULT_OK){
			Log.d(TAG, "DocumentActivity - onActivityResult (RESULT_OK)");
			finish();
		}
	}

	


	@Override
	public void onBackPressed() {
		finish();
	}

	@Override
	public void finish() {
		Intent intent = getIntent();
		setResult(RESULT_OK, intent);
		super.finish();
	}
	
	
	
	
	
	
}
