package kr.swmaestro.swmaestro.other;

import java.util.ArrayList;

import kr.swmaestro.swmaestro.data.DataUser;


public class CommonFunction {
	public static String getUserListString(ArrayList<DataUser> dataUserList){
		String userListText = "";
		for(int i=0; i<dataUserList.size(); i++){
			DataUser curUser = dataUserList.get(i);
			userListText += curUser.getName();
			if(i != dataUserList.size()-1){
				userListText += ", ";
			}
		}
		
		return userListText;
	}
}