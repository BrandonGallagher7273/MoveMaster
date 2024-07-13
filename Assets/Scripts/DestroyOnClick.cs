using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class DestroyOnClick : MonoBehaviour
{
    void Start() {
        StartDelay();
    }
    public static Boolean started = false;

    public void StartDelay()
    {
        // Start the coroutine and pass the duration of the delay
        StartCoroutine(WaitAndExecute(5.0f)); // Wait for 5 seconds
    }

    // Coroutine method
    private IEnumerator WaitAndExecute(float waitTime)
    {
        // Wait for the specified duration
        yield return new WaitForSeconds(waitTime);

        // Code to execute after the delay
        started = true;
        Debug.Log("hey!\n");
    }
    
    private void OnMouseDown()
    {
        if (started == false) {
            Destroy(gameObject);
        }
    }
}
