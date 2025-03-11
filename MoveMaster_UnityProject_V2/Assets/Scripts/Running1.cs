using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class RunningUI : MonoBehaviour
{
    public TextMeshProUGUI runningUI;

    void Start()
    {
        Debug.Log("working!");
        runningUI = GameObject.Find("RunningUI")?.GetComponent<TextMeshProUGUI>();
        runningUI.text = "YAY!";
    }

    void Update()
    {
        if (runningUI == null) return;  // Prevent errors if runningUI is null
        
        Debug.Log("DestroyOnClick.started: " + DestroyOnClick.started);

        if (DestroyOnClick.started)
        {
            runningUI.text = "Running...";
        }
        else
        {
            runningUI.text = "";
        }
    }
}