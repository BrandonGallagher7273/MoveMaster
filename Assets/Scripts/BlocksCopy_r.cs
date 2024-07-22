using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BlocksCopy_4 : MonoBehaviour
{

    public GameObject prefab;
    public int blocks = 27;
    private Rigidbody rb;
    public List<GameObject> clones = new List<GameObject>();
    public String spawn_code = "111111111111111111111111111";
    public String temp_spawn_code = "111111111111111111111111111";
    private Boolean flag = false;
    void ChangeAttribute1(Boolean flag) {
        if (flag == false) {
            foreach (GameObject clone in clones) {
                if (clone != null) {
                    rb = clone.GetComponent<Rigidbody>();
                    rb.isKinematic = false;
                }
            }
        }
    }
    void ChangeAttribute2(Boolean flag) {
        if (flag == false) {
            foreach (GameObject clone in clones) {
                if (clone != null) {
                    rb = clone.GetComponent<Rigidbody>();
                    rb.isKinematic = true;
                }
            }
        }
    }
    void Start()
    {
        SpawnBlocks();
    }
    
    void Update() {
        if (DestroyOnClick.started == true) {
            ChangeAttribute1(flag);
            flag = true;
        } else {
            ChangeAttribute1(flag);
            flag = false;
        }
    }

    public void SpawnBlocks() {
        foreach (GameObject clone in clones) {
            Destroy(clone);
        }
        rb = prefab.GetComponentInChildren<Rigidbody>();
        rb.isKinematic = true;
        int count = 0;
        int spawned = 0;
        for (int i = 0; i < blocks/3; i++) {
            for (int p = 0; p < 3; p++) {
                if (spawn_code[spawned] == '1') {
                   GameObject clone = Instantiate(prefab);
                    clone.tag = "Selectable";
                    clone.transform.position = new Vector3(50.75f,.92f*count+.70f,49.25f+p*0.75f);
                    clones.Add(clone); 
                }
                spawned++;
            }
            count++;
        }
    }
}
