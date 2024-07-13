using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BlocksCopy : MonoBehaviour
{
    public GameObject prefab;
    public int blocks = 27;
    private Rigidbody rb;
    private List<GameObject> clones = new List<GameObject>();
    private Boolean flag = false;
    void ChangeAttribute(Boolean flag) {
        if (flag == false) {
            foreach (GameObject clone in clones) {
                if (clone != null) {
                    rb = clone.GetComponent<Rigidbody>();
                    rb.isKinematic = false;
                }
            }
        }
    }
    void Start()
    {
        int count = 0;
        rb = prefab.GetComponentInChildren<Rigidbody>();
        rb.isKinematic = true;
        for (int i = 0; i < blocks/3; i++) {
            for (int p = 0; p < 3; p++) {
                GameObject clone = Instantiate(prefab);
                clone.tag = "Selectable";
                clone.transform.position = new Vector3(50+p*0.75f,.92f*count+0.1f,50);
                clones.Add(clone);
            }
            count++;
        }

    }
    void Update() {
        if (DestroyOnClick.started == true) {
            ChangeAttribute(flag);
            flag = true;
        }
    }
 }


