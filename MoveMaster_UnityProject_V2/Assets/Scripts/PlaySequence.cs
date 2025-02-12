using System;
using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.TextCore;

public class PlaySequence : MonoBehaviour
{

    public static bool sequence_active = false;

    public GameObject start;
    public GameObject enter_code;
    public GameObject reset;
    public GameObject camera_button;
    public GameObject status;
    

    void Start()
    {
        start = GameObject.Find("Start Button");
        enter_code = GameObject.Find("Set Start Button");
        reset = GameObject.Find("Tower Reset Button");
        camera_button = GameObject.Find("Switch Camera");
        status = GameObject.Find("Valid_Check");
    }
    // Update is called once per frame
    void Update()
    {
        if (sequence_active == true) {
            StartSequence();
            sequence_active = false;
        } 
    }

    void StartSequence() {
        start.SetActive(false);
        enter_code.SetActive(false);
        reset.SetActive(false);
        camera_button.SetActive(false);
        status.SetActive(false);

        string code = CodeEntry.code; // Example input
        List<int> blocks = new List<int>();
        List<int> top = new List<int>();

        // Split the string by spaces
        string[] numbers = code.Split(' ');

        foreach (string num in numbers)
        {
            if (float.TryParse(num, out float value)) // Convert to float
            {
                int wholePart = (int)value; // Extract integer part
                int decimalPart = (int)((value - wholePart) * 10); // Extract decimal part

                blocks.Add(wholePart);
                top.Add(decimalPart);
            }
            else
            {
                Debug.LogError("Invalid number: " + num);
            }
        }

        // Print results for debugging
        Debug.Log("Blocks: " + string.Join(", ", blocks));
        Debug.Log("Top: " + string.Join(", ", top));
    }
}
