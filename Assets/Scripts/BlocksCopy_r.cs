using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class BlocksCopy_4 : MonoBehaviour
{

    public GameObject prefab;
    public int blocks = 27;
    private Rigidbody rb;
    public List<GameObject> clones = new List<GameObject>();
    private static List<char> spawn_code = Enumerable.Repeat('1', 27).ToList();
    public static List<char> temp_spawn_code = Enumerable.Repeat('1', 27).ToList();
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

    public void NewTempCode_r(List<char> code) {
        temp_spawn_code = new List<char>(code);
    }

    public void SetSpawnCode_r() {
        spawn_code = new List<char>(temp_spawn_code);
    }
    public void ResetSpawnCode_r() {
        spawn_code = Enumerable.Repeat('1', 27).ToList();
        temp_spawn_code = Enumerable.Repeat('1', 27).ToList();
        SpawnBlocks();
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
        int tag_i = 1;
        string tag_s;
        temp_spawn_code = new List<char>(spawn_code);
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
                    tag_s = tag_i.ToString();
                    clone.tag = tag_s;
                    clone.transform.position = new Vector3(50.75f,.90f*count+0.225f+0.45f,49.25f+p*0.75f);
                    clones.Add(clone); 
                    tag_i++;
                }
                spawned++;
            }
            count++;
        }
    }
}
