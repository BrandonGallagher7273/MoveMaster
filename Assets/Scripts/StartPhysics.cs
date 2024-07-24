using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StartPhysics : MonoBehaviour
{
    public MeshRenderer rend;
    void Start() {
        rend = GetComponent<MeshRenderer>();
    }
    void Update() {
        if (DestroyOnClick.started == false) {
            rend.enabled=true;
            transform.position = new Vector3(47f, 1f, 44f);
        } else {
            rend.enabled=false;
            transform.position = new Vector3(40.5f, 1f, 42f);
        }
    }
    private void OnMouseDown()
    {
        Debug.Log("cube works\n");
        DestroyOnClick.started = true;
    }
}
