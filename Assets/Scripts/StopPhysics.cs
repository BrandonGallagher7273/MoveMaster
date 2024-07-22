using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StopPhysics : MonoBehaviour
{
    public MeshRenderer rend;
    public GameObject player;
    void Start() {
        rend = GetComponent<MeshRenderer>();
        player = GameObject.Find("Player");
    }
    void Update() {
        if (DestroyOnClick.started == true) {
            rend.enabled=true;
            transform.position = new Vector3(45.5f, 1f, 42f);
        } else {
            rend.enabled=false;
            transform.position = new Vector3(40.5f, 1f, 42f);
        }
    }
    private void OnMouseDown()
    {
        Debug.Log("cube works2\n");
        DestroyOnClick.started = false;
        BlocksCopy bc_1 = player.GetComponent<BlocksCopy>();
        bc_1.SpawnBlocks();
        BlocksCopy_4 bc_2 = player.GetComponent<BlocksCopy_4>();
        bc_2.SpawnBlocks();
    }
}
