using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class DestroyOnClick : MonoBehaviour
{

    public GameObject player;
    
    void Start() {
        player = GameObject.Find("Player");
    }
    
    public static Boolean started = false;
    
    private void OnMouseDown()
    {
        if (started == false) {
            Destroy(gameObject);
            
        }
    }
}
