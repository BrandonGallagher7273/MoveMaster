using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StartPhysics : MonoBehaviour
{
    public MeshRenderer rend;
    public Renderer matRend;
    public Material start_mat;
    public Material stop_mat;
    public GameObject player;
    public bool clicked = false;
    void Start() {
        rend = GetComponent<MeshRenderer>();
        matRend = GetComponent<Renderer>(); 
        player = GameObject.Find("Player");
    }
    void Update() {
        if (DestroyOnClick.started == false) {
            matRend.material = start_mat;
            //transform.position = new Vector3(47f, 1f, 44f);
        } else {
            matRend.material = stop_mat;
            //transform.position = new Vector3(40.5f, 1f, 42f);
        }
    }
    private void OnMouseDown()
    {
        DestroyOnClick.started = true;
        matRend.material = stop_mat;
        if(clicked)
        {
            matRend.material = start_mat;
            Debug.Log("cube works2\n");
            DestroyOnClick.started = false;
            BlocksCopy bc_1 = player.GetComponent<BlocksCopy>();
            bc_1.SpawnBlocks();
            BlocksCopy_4 bc_2 = player.GetComponent<BlocksCopy_4>();
            bc_2.SpawnBlocks();
            clicked = false;
        }
        else
        {
            clicked = true;
        }
    }
}