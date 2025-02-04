using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SetStart : MonoBehaviour
{
    public GameObject player;
    void Start() {
        player = GameObject.Find("Player");
    }
    private void OnMouseDown() {
        BlockPlacement bc_1 = player.GetComponent<BlockPlacement>();
        bc_1.SpawnBlocks();
    }
}
