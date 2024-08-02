using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/* This script ensures that blocks cannot move while started == False. */
public class FreezeBlocks : MonoBehaviour
{
    private Rigidbody rb;

    private bool FrozenSent  = false;
    private bool UnfrozenSent = false;

    // Update is called once per frame
    void Update()
    {
        if(DestroyOnClick.started == false)
        {
            UnfrozenSent = false;
            rb = GetComponent<Rigidbody>();
            rb.constraints = RigidbodyConstraints.FreezeRotation;
            rb.constraints = RigidbodyConstraints.FreezePosition;
            if(!FrozenSent) {
                Debug.Log("Constraints have been frozen."); 
                FrozenSent = true;
            }
        }
        else
        {
            FrozenSent = false;
            rb.constraints = RigidbodyConstraints.None;
            if(!UnfrozenSent) {
                Debug.Log("Constraints have been unfrozen."); 
                UnfrozenSent = true;
            }
         }
    }
}