package kr.swmaestro.swmaestro.data;

import java.util.ArrayList;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class DataDocument {
	private JSONObject mJsonObject;
	
	private DataUser getNoneUser(){
		return new DataUser();
	}
	
	public DataDocument(JSONObject jsonObject){
		mJsonObject = jsonObject;
	}
	
	public int getDocumentId(){
		try {
			return getDocument().getInt("id");
		} catch (JSONException e) {
			e.printStackTrace();
			return 0;
		}
	}
	public String getDocumentType(){
		try {
			return getDocument().getString("doc_type");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}

	public String getCreated(){
		try {
			return getDocument().getString("created");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public String getDeadLine(){
		try {
			return getDocument().getString("deadline");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public boolean isSubmitted(){
		try {
			return getDocument().getBoolean("is_submitted");
		} catch (JSONException e) {
			e.printStackTrace();
			return false;
		}
	}
	
	public boolean isComplete(){
		try {
			return getDocument().getBoolean("is_complete");
		} catch (JSONException e) {
			e.printStackTrace();
			return false;
		}
	}
	
	public String getCompleteTime(){
		try {
			return getDocument().getString("complete_time");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public String getSubmitTime(){
		try {
			return getDocument().getString("submit_time");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public ArrayList<DataUser> getSignUserList(){
		ArrayList<DataUser> dataUserList = new ArrayList<DataUser>();
		try {
			JSONArray jsonArraySignUserList = getDocument().getJSONArray("sign_users");
			for(int i=0; i<jsonArraySignUserList.length(); i++){
				JSONObject jsonObjectCurrentSignUser = jsonArraySignUserList.getJSONObject(i);
				DataUser curDataUser = new DataUser(jsonObjectCurrentSignUser);
				dataUserList.add(curDataUser);
			}
			return dataUserList;
		} catch (JSONException e) {
			e.printStackTrace();
			return dataUserList;
		}
	}
	
	public ArrayList<DataUser> getSignedUserList(){
		ArrayList<DataUser> dataUserList = new ArrayList<DataUser>();
		try {
			JSONArray jsonArraySignUserList = getDocument().getJSONArray("signed_users");
			for(int i=0; i<jsonArraySignUserList.length(); i++){
				JSONObject jsonObjectCurrentSignUser = jsonArraySignUserList.getJSONObject(i);
				DataUser curDataUser = new DataUser(jsonObjectCurrentSignUser);
				dataUserList.add(curDataUser);
			}
			return dataUserList;
		} catch (JSONException e) {
			e.printStackTrace();
			return dataUserList;
		}
	}
	
	public DataUser getSubmitUser(){
		JSONObject jsonObjectSubmitUser;
		try {
			jsonObjectSubmitUser = getDocument().getJSONObject("submit_user");
			DataUser curDataUser = new DataUser(jsonObjectSubmitUser);
			return curDataUser;
		} catch (JSONException e) {
			e.printStackTrace();
			return getNoneUser();
		}
	}
	
	public JSONObject getDocument(){
		try {
			return mJsonObject.getJSONObject("document");
		} catch (JSONException e) {
			e.printStackTrace();
			return null;
		}
	}
	public Object getExtends(){
		if(getDocumentType().equals("멘토링 보고서")){
			try {
				return new MentoringReport(mJsonObject.getJSONObject("extends"));
			} catch (JSONException e) {
				e.printStackTrace();
				return null;
			}
		} else if(getDocumentType().equals("기부금 영수증")){
			try {
				return new DonationReceipt(mJsonObject.getJSONObject("extends"));
			} catch (JSONException e) {
				e.printStackTrace();
				return null;
			}
		}
		else{
			return null;
		}
	}
	
	public ArrayList<DataDocumentExtend> getDocumentExtendList(){
		ArrayList<DataDocumentExtend> datadocumentExtendList = new ArrayList<DataDocumentExtend>();
		if(this.getDocumentType().equals("멘토링 보고서")){
			MentoringReport curMentoringReport = (MentoringReport) this.getExtends();
//			datadocumentExtendList.add(new DataDocumentExtend("타입", curMentoringReport.getType()));
//			datadocumentExtendList.add(new DataDocumentExtend("프로젝트", curMentoringReport.getType()));
//			datadocumentExtendList.add(new DataDocumentExtend("멘토", curMentoringReport.getType()));
//			datadocumentExtendList.add(new DataDocumentExtend("멘티목록", curMentoringReport.getType()));
//			datadocumentExtendList.add(new DataDocumentExtend("멘토링 날짜", curMentoringReport.getType()));
//			datadocumentExtendList.add(new DataDocumentExtend("멘토링 장소", curMentoringReport.getType()));
			datadocumentExtendList.add(new DataDocumentExtend("시작시간", curMentoringReport.getStartTime()));
			datadocumentExtendList.add(new DataDocumentExtend("종료시간", curMentoringReport.getEndTime()));
			datadocumentExtendList.add(new DataDocumentExtend("실제시간", curMentoringReport.getRealTime()));
			datadocumentExtendList.add(new DataDocumentExtend("인정시간", curMentoringReport.getAcceptTime()));
			datadocumentExtendList.add(new DataDocumentExtend("보고서 주제", curMentoringReport.getTitle()));
			datadocumentExtendList.add(new DataDocumentExtend("보고서 내용", curMentoringReport.getContent()));
			datadocumentExtendList.add(new DataDocumentExtend("보고서 멘토의견", curMentoringReport.getOpinion()));
			datadocumentExtendList.add(new DataDocumentExtend("보고서 계획사항", curMentoringReport.getSchedule()));
			datadocumentExtendList.add(new DataDocumentExtend("보고서 특이사항", curMentoringReport.getIssue()));
			return datadocumentExtendList;
		}
		else if(this.getDocumentType().equals("기부금 영수증")){
			DonationReceipt curDonationReceipt = (DonationReceipt) this.getExtends();
			datadocumentExtendList.add(new DataDocumentExtend("연도", curDonationReceipt.getYear()));
			datadocumentExtendList.add(new DataDocumentExtend("월", curDonationReceipt.getMonth()));
			return datadocumentExtendList;
		}
		else{
			return datadocumentExtendList;
		}
		
	}
	
	
	
	class MentoringReport{
		private JSONObject mJsonObject;
		
		public MentoringReport(JSONObject jsonObject){
			mJsonObject = jsonObject;
		}
		
		public String getType(){
			try {
				return mJsonObject.getString("type");
			} catch (JSONException e) {
				e.printStackTrace();
				return "";
			}
		}
		
		public String getProject(){
			try {
				return mJsonObject.getString("project");
			} catch (JSONException e) {
				e.printStackTrace();
				return "";
			}
		}
		
		public DataUser getMentor(){
			JSONObject jsonObjectMentor;
			try {
				jsonObjectMentor = mJsonObject.getJSONObject("mentor");
				DataUser curDataUser = new DataUser(jsonObjectMentor);
				return curDataUser;
			} catch (JSONException e) {
				e.printStackTrace();
				return new DataUser("");
			}
		}
		
		public ArrayList<DataUser> getMenteeList(){
			ArrayList<DataUser> dataUserList = new ArrayList<DataUser>();
			try {
				JSONArray jsonArrayMenteeList = mJsonObject.getJSONArray("mentees");
				for(int i=0; i<jsonArrayMenteeList.length(); i++){
					JSONObject jsonObjectCurrentMentee = jsonArrayMenteeList.getJSONObject(i);
					DataUser curDataUser = new DataUser(jsonObjectCurrentMentee);
					dataUserList.add(curDataUser);
				}
				return dataUserList;
			} catch (JSONException e) {
				e.printStackTrace();
				return dataUserList;
			}
		}
		
		public String getDate(){
			try {
				return mJsonObject.getString("date");
			} catch (JSONException e) {
				e.printStackTrace();
				return "";
			}
		}
		
		public String getPlace(){
			try {
				return mJsonObject.getString("place");
			} catch (JSONException e) {
				e.printStackTrace();
				return "";
			}
		}
		
		public String getStartTime(){
			try {
				return mJsonObject.getString("start_time");
			} catch (JSONException e) {
				e.printStackTrace();
				return "";
			}
		}
		
		public String getEndTime(){
			try {
				return mJsonObject.getString("end_time");
			} catch (JSONException e) {
				e.printStackTrace();
				return "";
			}
		}
		
		public String getRealTime(){
			try {
				return mJsonObject.getString("real_time");
			} catch (JSONException e) {
				e.printStackTrace();
				return "";
			}
		}
		
		public String getAcceptTime(){
			try {
				return mJsonObject.getString("accept_time");
			} catch (JSONException e) {
				e.printStackTrace();
				return "";
			}
		}
		
		public String getTitle(){
			try {
				return mJsonObject.getString("title");
			} catch (JSONException e) {
				e.printStackTrace();
				return "";
			}
		}
		
		public String getContent(){
			try {
				return mJsonObject.getString("content");
			} catch (JSONException e) {
				e.printStackTrace();
				return "";
			}
		}
		
		public String getOpinion(){
			try {
				return mJsonObject.getString("opinion");
			} catch (JSONException e) {
				e.printStackTrace();
				return "";
			}
		}
		
		public String getSchedule(){
			try {
				return mJsonObject.getString("schedule");
			} catch (JSONException e) {
				e.printStackTrace();
				return "";
			}
		}
		
		public String getIssue(){
			try {
				return mJsonObject.getString("issue");
			} catch (JSONException e) {
				e.printStackTrace();
				return "";
			}
		}
		
		public String get(){
			try {
				return mJsonObject.getString("");
			} catch (JSONException e) {
				e.printStackTrace();
				return "";
			}
		}
	}
	class DonationReceipt{
		private JSONObject mJsonObject;
		
		public DonationReceipt(JSONObject jsonObject) {
			mJsonObject = jsonObject;
		}

		public String getYear(){
			try {
				return mJsonObject.getString("year");
			} catch (JSONException e) {
				e.printStackTrace();
				return "";
			}
		}
		
		public String getMonth(){
			try {
				return mJsonObject.getString("month");
			} catch (JSONException e) {
				e.printStackTrace();
				return "";
			}
		}
	}
}
