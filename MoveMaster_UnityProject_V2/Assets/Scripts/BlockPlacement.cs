using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class BlockPlacement : MonoBehaviour
{
    public GameObject prefab;
    public int blocks = 54;
    private Rigidbody rb;
    public List<GameObject> clones = new List<GameObject>();
    private Boolean flag = false;

    //turns physics ON
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
    //turns physics OFF
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
            ChangeAttribute2(flag);
            flag = false;
        }
    }

    public void SpawnBlocks() {
        int tag_i = 1;
        string tag_s;
        foreach (GameObject clone in clones) {
            Destroy(clone);
        }
        int count = 0;
        int spawned = 0;
        rb = prefab.GetComponentInChildren<Rigidbody>();
        rb.isKinematic = true;
        for (int i = 0; i < blocks/6; i++) {
            for (int p = 0; p < 3; p++) {
                tag_s = tag_i.ToString();
                GameObject clone = Instantiate(prefab);
                clone.tag = tag_s;
                clone.transform.Rotate(0, 90, 0);
                clone.transform.position = new Vector3(50+p*0.75f,.90f*count+0.225f,50);
                clones.Add(clone);
                tag_i++;
                spawned++;
            }
            for (int p = 0; p < 3; p++) {
                tag_s = tag_i.ToString();
                GameObject clone = Instantiate(prefab);
                clone.tag = tag_s;
                clone.transform.position = new Vector3(50.75f,.90f*count+0.225f+0.45f,49.25f+p*0.75f);
                clones.Add(clone);
                tag_i++;
                spawned++;
            }
            count++;
        }
        
    }
}
