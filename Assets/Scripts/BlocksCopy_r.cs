using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BlocksCopy_4 : MonoBehaviour
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
        rb = prefab.GetComponentInChildren<Rigidbody>();
        rb.isKinematic = true;
        int count = 0;
        for (int i = 0; i < blocks/3; i++) {
            for (int p = 0; p < 3; p++) {
                GameObject clone = Instantiate(prefab);
                clone.tag = "Selectable";
                clone.transform.position = new Vector3(50.75f,.92f*count+.55f,49.25f+p*0.75f);
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
